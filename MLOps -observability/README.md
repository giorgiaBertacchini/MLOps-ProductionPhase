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

## Tools

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/tools.png)

## Tools & Ports

| Tool | Port |
| --- | --- |
| Bento | `localhost:3005` |
| Evidently Service | `localhost:8085` |
| Prometheus | `localhost:9090` |
| Alertmanager | `localhost:9093` |
| Grafana | `localhost:3000` |
| Streamlit App | `localhost:8501` |


## Schema
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/schema.png)

## Connections
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/comunications.png)

## Run
To up and start docker images:
```
docker compose up
```
In Docker desktop appear these images: `prom/prometheus`, `grafana/grafana`, `mlops-observability-evidently_service`, `prom/alertmanager`. Also this command run `bento` image about the ml model.

## Streamlit app

To run the streamlit app:
```
streamlit run .\metrics_app\streamlit_app.py
```

From this application the users can:

- require predictions
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_Predictions.png)

- find directly link to observation tools
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_Monitor.png)

- run to retrain the ml model or run single actions usefull
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_CompleteRetrain.png)


## Changes
```
docker compose down
```

In Docker desktop cancel the three images.

```
docker compose up
```
