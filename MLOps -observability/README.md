<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#mlops-observability">MLOps observability</a>
    </li>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#schema">Schema</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-it-works">How it works</a></li>
      <ul>
        <li><a href="#drift-and-model-monitoring">Drift and model monitoring</a></li>
        <li><a href="#systems-monitoring-and-alerting">Systems monitoring and alerting</a></li>
        <li><a href="#alert-management">Alert management</a></li>
        <li><a href="#managed-observability-platform">Managed observability platform</a></li>
      </ul>
    </li>
    <li>
      <a href="#bridge">Bridge</a>
      <ul>
        <li><a href="#interactions-and-communication">Interactions And Communication</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#acknowledgments">Acknowledgments</a>
    </li>
  </ol>
</details>

# MLOps observability

:books: *Theory: Model monitoring: The model predictive performance is monitored to potentially invoke a new iteration in the ML process.*

# About The Project

This is the implementation of MLOps observability system.

It is think to used during the production, after the setup of machine learning model.

## Built with

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/tools.png)

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

# How it works
The ML model is a docker image `Bentoml` tool, by Development sector that have train and build the ml model.

The monitoring is do by tools: `Evidently`, `Prometheus`. These observe the ML model work, in particular:
- `Evidently` search data and model drift,
- `Prometheus` check metrics to server level, so throughput, time spend, request count. Plus this tool group metrics generate by `Evidently`, `Alermanager` and `Bentoml` service from their `/metrics` link.

To send alert message, `Alertmanager` tool when receive alerts from `Prometheus` send a mesage on 'Monitoring' channel of Slack chat.

To show all these metrics `Grafana` tool provide a dashboard customizable and real-time, so through graphs display data received from `Prometheus`.

`DVC` tool is used to download from `Google Drive` the dataset on which ml model is trained.

## Streamlit app

To run the streamlit app:
```
streamlit run .\metrics_app\streamlit_app.py
```


## Drift and model monitoring

<div align="center">
  <img width="300" alt="evidently logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/evidently_logo.png">
</div>

[Evidently](https://www.evidentlyai.com/)

## Systems monitoring and alerting
<div align="center">
  <img width="300" alt="prometheus logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/prometheus_logo.png">
</div>

[Prometheus](https://prometheus.io/docs/introduction/overview/)

From this tool the user can make query to receive metrics grouped by it.


## Alert management

<div align="center">
  <img width="120" alt="alermanager logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/alermanager_logo.png">
</div>

[Alermanager](https://prometheus.io/docs/alerting/latest/overview/)

## Managed observability platform

<div align="center">
  <img width="140" alt="grafana logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/grafana_logo.svg.png">
</div>

[Grafana](https://grafana.com/)

From this tool the users can create own dashboard with graphs personalized.

## Building application
<div align="center">
  <img width="260" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_logo.png">
</div>

[Streamlit](https://streamlit.io/)

# Bridge

## Interactions And Communication

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/comunications.png)

## Getting Started

To up and start docker images:
```
docker compose up
```
In Docker desktop appear these images: `prom/prometheus`, `grafana/grafana`, `mlops-observability-evidently_service`, `prom/alertmanager`. Also this command run `bento` image about the ml model.

## Prerequisites
## Installation

# Usage

## Streamlit App

From this application the users can:

- require predictions,

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_Predictions.png)

- find directly link to observation tools,

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_Monitor.png)

- run to retrain the ml model or run single actions usefull.

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_CompleteRetrain.png)

## Prometheus Dashboard
![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/prometheus.png)

From its `/alerts` the user can see the alert active and which is verified.

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/prometheus_alert.png)

## AlerManager Dashboard



In the next image you can see a example of an alert message sent to a chat Slack.

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/chatSlack.png)

## Grafana Dashboard

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/grafana.png)



# Acknowledgments
