# MLOps - observability

## What is
This is the implementation of MLOps observability system.

## Where is used
It is think to used during the production, after the setup of machine learning model.

## How work
The ML model is a docker image `Bentoml` tool, by Development sector that have train and build the ml model.

The monitoring is do by tools: `Evidently`, `Prometheus`. These observe the ML model work, in particular:
- `Evidently` search data and model drift,
- `Prometheus` check metrics to server level, so throughput, time spend, request count. Plus this tool group metrics generate by `Evidently`, `Alermanager` and `Bentoml` service from their `/metrics` link.

To send alert message, `Alertmanager` tool when receive alerts from `Prometheus` send a mesage on 'Monitoring' channel of Slack chat.

To show all these metrics `Grafana` tool provide a dashboard customizable and real-time, so through graphs display data received from `Prometheus`.

`DVC` tool is used to download from `Google Drive` the dataset on which ml model is trained.

## Run
To up and start docker images:
```
docker compose up
```
In Docker desktop appear these images: `prom/prometheus`, `grafana/grafana`, `mlops-observability-evidently_service`, `prom/alertmanager`.

To run the streamlit app:
```
streamlit run .\metrics_app\streamlit_app.py
```

## Tools & Ports

| Tool | Port |
| --- | --- |
| Bento | `localhost:3005` |
| Evidently Service | `localhost:8085` |
| Prometheus | `localhost:9090` |
| Alertmanager | `localhost:9093` |
| Grafana | `localhost:3000` |
| Streamlit App | `localhost:8501` |

Bento:
`localhost:3005`

Streamlit App:
`localhost:8501`

Evidently Service:
`localhost:8085`
`localhost:8085/metrics`
`localhost:8085/drift_report`
`localhost:8085/data_stability`
`localhost:8085/data_drift_tests`

Prometheus:
`localhost:9090`

Grafana:
`localhost:3000`

## Changes
```
docker compose down
```

In Docker desktop cancel the three images.

```
docker compose up
```
