#!/usr/bin/env python3
"""
Data generator for OpenEgiz Oven digital twins (oven-01, oven-02).

Sends simulated telemetry data via MQTT (Mosquitto) using the Eclipse Ditto protocol.
Features: voltage_v, current_a, active_power_kw, power_factor.
"""

import argparse
import json
import math
import random
import signal
import sys
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


# ── Default configuration ────────────────────────────────────────────
DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 30511
DEFAULT_THING_IDS = [
    "org.openegiz:oven-01",
    "org.openegiz:oven-02",
]
DEFAULT_INTERVAL = 5  # seconds


# ── Realistic value simulation ───────────────────────────────────────

class OvenSimulator:
    """Simulates realistic electrical parameters for an industrial oven."""

    def __init__(self):
        self._step = 0
        # Base values
        self._base_voltage = 220.0
        self._base_current = 20.0
        self._base_pf = 0.92
        # Oven cycle period (in steps) — ~5 minute heating cycle
        self._cycle_period = 60

    def generate(self) -> dict:
        """Generate one set of readings."""
        self._step += 1
        t = self._step

        # Phase in the heating cycle (0 to 2π)
        phase = (2 * math.pi * t) / self._cycle_period

        # Voltage: ~220V with small grid fluctuations (σ=2V)
        voltage = self._base_voltage + random.gauss(0, 2.0)
        voltage = round(max(200.0, min(240.0, voltage)), 2)

        # Current: sinusoidal heating cycle (ramp up → hold → ramp down)
        # Range roughly 8A to 45A
        cycle_factor = 0.5 + 0.5 * math.sin(phase)  # 0..1
        current = 8.0 + cycle_factor * 37.0 + random.gauss(0, 1.5)
        current = round(max(5.0, min(50.0, current)), 2)

        # Power factor: varies slightly with load
        # Higher load → slightly better PF
        pf = self._base_pf + 0.05 * cycle_factor + random.gauss(0, 0.01)
        pf = round(max(0.75, min(0.99, pf)), 3)

        # Active power: P = V × I × PF / 1000 (in kW)
        active_power = (voltage * current * pf) / 1000.0
        active_power = round(active_power, 3)

        return {
            "voltage_v": voltage,
            "current_a": current,
            "active_power_kw": active_power,
            "power_factor": pf,
        }


# ── Ditto protocol message builder ──────────────────────────────────

def build_ditto_message(thing_id: str, features: dict) -> dict:
    """
    Build an Eclipse Ditto protocol envelope to update all features.

    Topic format: {namespace}/{name}/things/twin/commands/modify
    Path: /features
    """
    namespace, name = thing_id.split(":", 1)

    # Add timestamp to each feature
    now = datetime.now(timezone.utc).isoformat()
    ditto_features = {}
    for feat_name, feat_value in features.items():
        ditto_features[feat_name] = {
            "properties": {
                "value": feat_value,
                "timestamp": now,
            }
        }

    return {
        "topic": f"{namespace}/{name}/things/twin/commands/modify",
        "path": "/features",
        "value": ditto_features,
    }


# ── MQTT publisher ───────────────────────────────────────────────────

class MqttPublisher:
    """Publishes Ditto protocol messages to Mosquitto."""

    def __init__(self, host: str, port: int, thing_id: str):
        self.host = host
        self.port = port
        self.thing_id = thing_id
        # MQTT topic that Ditto's mosquitto-source-connection listens on
        self.topic = f"telemetry/{thing_id}"

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"oven-data-gen-{random.randint(1000,9999)}",
            protocol=mqtt.MQTTv5,
        )
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.connected = False

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0 or (hasattr(rc, 'value') and rc.value == 0):
            self.connected = True
            print(f"✅ Подключено к MQTT брокеру {self.host}:{self.port}")
        else:
            print(f"❌ Ошибка подключения к MQTT: код={rc}")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        self.connected = False
        print(f"⚠️  Отключено от MQTT брокера (код={rc})")

    def connect(self):
        """Connect to the MQTT broker."""
        print(f"🔌 Подключение к Mosquitto ({self.host}:{self.port})...")
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()
        # Wait briefly for connection
        for _ in range(10):
            if self.connected:
                break
            time.sleep(0.5)
        if not self.connected:
            print("❌ Не удалось подключиться к MQTT брокеру!")
            sys.exit(1)

    def publish(self, message: dict):
        """Publish a Ditto protocol message."""
        payload = json.dumps(message)
        result = self.client.publish(self.topic, payload, qos=0)
        result.wait_for_publish(timeout=5)

    def disconnect(self):
        """Disconnect from the broker."""
        self.client.loop_stop()
        self.client.disconnect()
        print("🔌 Отключено от MQTT брокера")


# ── Main loop ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Генератор данных для цифрового двойника печи (OpenEgiz)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 data_generator.py
  python3 data_generator.py --interval 2
  python3 data_generator.py --mqtt-host 192.168.1.100 --mqtt-port 1883
        """,
    )
    parser.add_argument(
        "--mqtt-host", default=DEFAULT_MQTT_HOST,
        help=f"Адрес MQTT-брокера (по умолчанию: {DEFAULT_MQTT_HOST})",
    )
    parser.add_argument(
        "--mqtt-port", type=int, default=DEFAULT_MQTT_PORT,
        help=f"Порт MQTT-брокера (по умолчанию: {DEFAULT_MQTT_PORT})",
    )
    parser.add_argument(
        "--thing-ids", nargs="+", default=DEFAULT_THING_IDS,
        help=f"ID вещей в Ditto (по умолчанию: {' '.join(DEFAULT_THING_IDS)})",
    )
    parser.add_argument(
        "--interval", type=float, default=DEFAULT_INTERVAL,
        help=f"Интервал отправки данных в секундах (по умолчанию: {DEFAULT_INTERVAL})",
    )

    args = parser.parse_args()

    # Setup simulators and MQTT publishers for each twin
    twins = []
    for thing_id in args.thing_ids:
        sim = OvenSimulator()
        pub = MqttPublisher(args.mqtt_host, args.mqtt_port, thing_id)
        twins.append({"id": thing_id, "simulator": sim, "publisher": pub})

    # Graceful shutdown
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("\n🛑 Остановка генератора...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Connect all publishers
    for twin in twins:
        twin["publisher"].connect()

    print(f"\n🏭 Генератор данных для {len(twins)} двойников:")
    for twin in twins:
        print(f"   📡 {twin['id']} → telemetry/{twin['id']}")
    print(f"⏱️  Интервал: {args.interval}с")
    header = f"{'Время':<12} {'Twin':<25} {'Напр.(V)':<10} {'Ток(A)':<10} {'Мощн.(kW)':<12} {'Cosφ':<8}"
    print(f"{'─' * len(header)}")
    print(header)
    print(f"{'─' * len(header)}")

    count = 0
    try:
        while running:
            ts = datetime.now().strftime("%H:%M:%S")

            for twin in twins:
                # Generate data
                readings = twin["simulator"].generate()

                # Build & publish Ditto message
                message = build_ditto_message(twin["id"], readings)
                twin["publisher"].publish(message)

                count += 1
                print(
                    f"{ts:<12} "
                    f"{twin['id']:<25} "
                    f"{readings['voltage_v']:<10} "
                    f"{readings['current_a']:<10} "
                    f"{readings['active_power_kw']:<12} "
                    f"{readings['power_factor']:<8}"
                )

            time.sleep(args.interval)

    finally:
        for twin in twins:
            twin["publisher"].disconnect()
        print(f"\n📊 Всего отправлено сообщений: {count}")


if __name__ == "__main__":
    main()
