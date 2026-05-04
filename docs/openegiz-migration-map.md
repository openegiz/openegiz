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

## Runtime artifact URLs

| Artifact | URL |
| --- | --- |
| Helm repository | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts` |
| OpenEgiz Grafana app zip | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts/plugins/openegiz-openegiz-app.zip` |
| OpenEgiz Unity panel zip | `https://raw.githubusercontent.com/openegiz/helm-charts/codex/bootstrap-openegiz-helm-charts/plugins/openegiz-unity-panel.zip` |
| Ditto Extended API image | `ghcr.io/openegiz/ditto-extended-api` |
| Kafka-ML images | `ghcr.io/openegiz/kafka-ml-*` |

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
