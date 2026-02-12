.PHONY: install uninstall status endpoints upgrade upload-build generate-data

RELEASE_NAME := openegiz
CHART_PATH   := .

## Install the OpenEgiz Helm chart
install:
	helm install $(RELEASE_NAME) $(CHART_PATH) --wait --timeout=15m --debug

## Upgrade the OpenEgiz Helm chart
upgrade:
	helm upgrade $(RELEASE_NAME) $(CHART_PATH) --wait --timeout=15m --debug

## Uninstall the OpenEgiz Helm chart
uninstall:
	helm uninstall $(RELEASE_NAME)

## Show pod statuses
status:
	@kubectl get pods -o wide

## Show all service endpoints (IP + port)
endpoints:
	@bash scripts/show-endpoints.sh

## Upload Unity WebGL build files to the nginx pod
upload-build:
	@bash scripts/upload-build.sh $(RELEASE_NAME)

## Run the data generator for oven twins
generate-data:
	@bash -c 'source data-generator/venv/bin/activate && python3 data-generator/data_generator.py'
