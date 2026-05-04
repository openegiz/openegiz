# OpenEgiz Migration Map

This branch moves OpenEgiz to OpenEgiz-owned runtime download points and source repositories.

## OpenEgiz-owned repositories

| Component | Repository | Branch |
| --- | --- | --- |
| Platform Helm chart | `https://github.com/openegiz/openegiz` | `codex/rebrand-openegiz` |
| Helm chart artifacts and Grafana plugin zips | `https://github.com/openegiz/helm-charts` | `codex/bootstrap-openegiz-helm-charts` |
| Grafana app plugin | `https://github.com/openegiz/openegiz-in-grafana` | `codex/openegiz-rebrand` |
| Grafana Unity panel | `https://github.com/openegiz/grafana-panel-unity` | `codex/openegiz-rebrand` |
| Ditto Extended API | `https://github.com/openegiz/ditto-extended-api` | `codex/openegiz-rebrand` |
| Kafka-ML | `https://github.com/openegiz/kafka-ml` | `codex/openegiz-rebrand` |

## Runtime inventory

| Component | Runtime source | Ownership | Status |
| --- | --- | --- | --- |
| Platform Helm chart | `https://github.com/openegiz/openegiz` | OpenEgiz | Main install source for this branch. |
| Helm dependency repository | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts` | OpenEgiz | `make deps`, `make install`, and `make upgrade` fetch dependencies from this repository. |
| Grafana app plugin zip | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts/plugins/openegiz-openegiz-app.zip` | OpenEgiz | Plugin ID `openegiz-openegiz-app`, name `OpenEgiz`, author `OpenEgiz`, logo `img/logo.svg`. |
| Grafana Unity panel zip | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts/plugins/openegiz-unity-panel.zip` | OpenEgiz | Plugin ID `openegiz-unity-panel`, author `OpenEgiz`, logo `img/logo.svg`. |
| Ditto Extended API image | `ghcr.io/openegiz/ditto-extended-api:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML backend image | `ghcr.io/openegiz/kafka-ml-backend:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML frontend image | `ghcr.io/openegiz/kafka-ml-frontend:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML Kafka control logger image | `ghcr.io/openegiz/kafka-ml-kafka_control_logger:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML PyTorch executor image | `ghcr.io/openegiz/kafka-ml-pthexecutor:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML TensorFlow executor image | `ghcr.io/openegiz/kafka-ml-tfexecutor:latest` | OpenEgiz | Public anonymous pull verified. |
| Kafka-ML PyTorch training image | `ghcr.io/openegiz/kafka-ml-pytorch_model_training:latest` | OpenEgiz | Public anonymous pull verified; used by Kafka-ML runtime config. |
| Kafka-ML TensorFlow training image | `ghcr.io/openegiz/kafka-ml-tensorflow_model_training:latest` | OpenEgiz | Public anonymous pull verified; used by Kafka-ML runtime config. |
| Kafka-ML PyTorch inference image | `ghcr.io/openegiz/kafka-ml-pytorch_model_inference:latest` | OpenEgiz | Public anonymous pull verified; used by Kafka-ML runtime config. |
| Kafka-ML TensorFlow inference image | `ghcr.io/openegiz/kafka-ml-tensorflow_model_inference:latest` | OpenEgiz | Public anonymous pull verified; used by Kafka-ML runtime config. |

## Third-party foundation

These components intentionally keep their upstream product names. OpenEgiz does not rebrand or fork their product identity; it only serves the packaged dependency charts through the OpenEgiz Helm artifact repository above.

| Component | Why it stays third-party |
| --- | --- |
| Eclipse Ditto | Digital twin backend dependency. |
| Eclipse Hono | Optional IoT messaging dependency. |
| Grafana | UI runtime that loads the OpenEgiz plugins. |
| MongoDB | Ditto persistence dependency. |
| InfluxDB | Time-series storage dependency. |
| Telegraf | Metrics/stream collector dependency. |
| Mosquitto | MQTT broker dependency. |

## Active OpenEgiz names

| Surface | OpenEgiz value |
| --- | --- |
| Grafana app plugin ID | `openegiz-openegiz-app` |
| Unity panel plugin ID | `openegiz-unity-panel` |
| Grafana datasource | `openegiz` |
| MQTT target topic | `openegiz/#` |
| Kafka target topic | `openegiz` |
| InfluxDB organization | `openegiz` |
| Helm template helpers | `openegiz.*` |
| Internal job mount paths | `/var/run/openegiz/...` |

The source tree no longer vendors third-party dependency charts under `charts/`. `make deps`, `make install`, and `make upgrade` add the OpenEgiz Helm artifact repository and fetch dependencies from the OpenEgiz-owned raw GitHub branch above.

Third-party infrastructure components such as Eclipse Ditto, Eclipse Hono, Grafana, MongoDB, InfluxDB, Telegraf, and Mosquitto keep their upstream product identities. Their packaged Helm chart downloads are now served from the OpenEgiz Helm artifact repository branch above.
