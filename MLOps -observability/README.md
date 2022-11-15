<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#mlops-observability">MLOps observability</a>
      <ul>
        <li><a href="#notifications">Notifications</a></li>
        <li><a href="#drift-detection">Drift Detection</a></li>
      </ul>
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
        <li><a href="#01-drift-and-model-monitoring">01 Drift and model monitoring</a></li>
        <ul>
          <li><a href="#01-collaboration">01 Collaboration</a></li>
          <li><a href="#01-key-elements">01 Key Elements</a></li>
          <ul>
            <li><a href="#tests">Tests</a></li>
            <li><a href="#reports">Reports</a></li>
            <li><a href="#monitors">Monitors</a></li>
          </ul>
        </ul>
        <li><a href="#02-systems-monitoring-and-alerting">02 Systems monitoring and alerting</a></li>        
        <ul>
          <li><a href="#02-collaboration">02 Collaboration</a></li>
          <li><a href="#02-structure">02 Structure</a></li>
          <li><a href="#02-key-elements">02 Key Elements</a></li>
          <li><a href="#02-guidelines">02 Guidelines</a></li>
        </ul>
        <li><a href="#03-alert-management">03 Alert management</a></li>
        <li><a href="#04-managed-observability-platform">04 Managed observability platform</a></li>     
        <li><a href="#05-building-application">04 Building application</a></li>
        <ul>
          <li><a href="#05-structure">05 Structure</a></li>
          <li><a href="#05-key-elements">05 Key Elements</a></li>
        </ul>
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

Once the ML model has been deployed, it need to be monitored to assure that the ML model performs as expected. 

The process of observing the ML model performance based on live and previously unseen data. In particular, we are interested in ML-specific signals, such as prediction deviation from previous model performance. These signals might be used as triggers for model re-training.

Machine learning models need to be monitored at two levels:
* at the resource level, including ensuring the model is running correctly in the production environment. It's a traditional DevOps topic. Just as for any application running on a server, collecting IT metrics such as CPU, memory, disk, or network usage can be useful to detect and troubleshoot issues.
* at the performance level, meaning monitoring the pertinence of the model over time. Model performance monitoring attempts to track this degradation, and, at an appropriate time, it will also trigger the retraining of the model with more representative data. This is about analyzing the accuracy of the model.

## Notifications
It’s important to note that the goal of notifications is not necessarily to kick off an automated process of retraining, validation, and deployment. Model performance can change for a variety of reasons, and retraining may not always be the answer. The point is to alert the data scientist of the change; that person can then diagnose the issue and evaluate the next course of action.

Practically, every deployed model should come with monitoring metrics and corresponding warning thresholds to detect meaningful business performance drops as quickly as possible.

## Drift Detection
* Label drift: output data shifts (Target drift)
* Feature drift: input data shifts (Features drift)

Input drift is based on the principle that a model is only going to predict accurately if the data it was trained on is an accurate reflection of the real world. 


# About The Project

This is the implementation of MLOps observability system.

It is think to used during the production, after the setup of machine learning model.

## Built with

<div align="center">
  <img width="700" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/mon_tools.png">
</div>

| Tool | Port |
| --- | --- |
| Bento | `localhost:3005` |
| Evidently Service | `localhost:8085` |
| Prometheus | `localhost:9090` |
| Alertmanager | `localhost:9093` |
| Grafana | `localhost:3000` |
| Streamlit App | `localhost:8501` |

## Schema

<div align="center">
  <img width="700" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/schema.png">
</div>

# How it works
The ML model is a docker image `Bentoml` tool, by Development sector that have train and build the ml model.

The monitoring is do by tools: `Evidently`, `Prometheus`. These observe the ML model work, in particular:
- `Evidently` search data and model drift,
- `Prometheus` check metrics to server level, so throughput, time spend, request count. Plus this tool group metrics generate by `Evidently`, `Alermanager` and `Bentoml` service from their `/metrics` link.

To send alert message, `Alertmanager` tool when receive alerts from `Prometheus` send a mesage on 'Monitoring' channel of Slack chat.

To show all these metrics `Grafana` tool provide a dashboard customizable and real-time, so through graphs display data received from `Prometheus`.

`DVC` tool is used to download from `Google Drive` the dataset on which ml model is trained.

## 01 Drift and model monitoring

<div align="center">
  <img width="300" alt="evidently logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/evidently_logo.png">
</div>

:books: *Theory: The logic is that if the data distribution (e.g., mean, standard deviation, correlations between features) diverges between the training and testing phases on one side and the development phase on the other, it is a strong signal that the model’s performance won’t be the same.*

[Evidently](https://www.evidentlyai.com/) helps evaluate, test, and monitor the performance of ML models from validation to production.

The tool generates interactive reports from pandas DataFrame. 

### 01 Collaboration
Evidently have two integrations:
* Evidently with MLflow
* Evidently with Grafana and Prometheus

#### Evidently with MLflow
You use Evidently to calculate the metrics and MLflow to log the results. You can then access the metrics in the MLflow interface.

#### Evidently with Grafana and Prometheus
Evidently provides a metrics calculation layer, Prometheus is used to store the metrics, and Grafana is used to display the dashboards and manage alerts.

<div align="center">
  <img width="650" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/integration.png">
</div>

### 01 Key Elements
Evidently has three components: Reports, Tests, and Monitors (in development). 

#### Tests
* Tests perform structured data and ML model quality checks. You typically compare two datasets: reference and current.
* Required input: one or two datasets as pandas.DataFrames or csv.
* How you get the output: as an HTML inside Jupyter notebook or Colab, as an exportable HTML file, as a JSON, or as a Python dictionary.

#### Reports
* Reports calculate various metrics and provide rich interactive visualizations.
* Required input: one or two datasets as pandas.DataFrames or csv.
* How you get the output: as an HTML inside Jupyter notebook or Colab, as an exportable HTML file, as JSON, or as a Python dictionary.

#### Monitors
* Evidently also has Monitors that collect data and model metrics from a deployed ML service.
* You can use configuration to define the monitoring logic. Evidently calculates the metrics over the streaming data and emits them in Prometheus format. There are pre-built Grafana dashboards to visualize them.
* Required input: POST live data from the ML service.
* How you get the output: data and quality metrics in the Prometheus format.

## 02 Systems monitoring and alerting
<div align="center">
  <img width="300" alt="prometheus logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/prometheus_logo.png">
</div>

:books: *Theory: Monitoring models need to collect metrics and to quere on they.*

[Prometheus](https://prometheus.io/docs/introduction/overview/) is a platform for monitoring application metrics and generating alerts for these metrics.
From this tool the user can make query to receive metrics grouped by it.

Prometheus is Docker and Kubernetes compatible and available on the Docker Hub.
The Prometheus server has its own self-contained unit that does not depend on network storage or external services. So it doesn’t require a lot of work to deploy additional infrastructure or software.

Which units are monitored of those target?
* CPU status
* requests count
* request duration
* memory usage

But also collect metrics from Evidently source to provide also drift detection data.

### 02 Collaboration

BentoML offer a integration with Prometheus.

So Prometheus monitor and take metrics about the BentoML service from /metrics endpoint, which includes the essential metrics for model serving and the ability to create and customize new metrics base on needs.

This guide will introduce how to use Prometheus and Grafana to monitor your BentoService: [docs.bentoml.org/en/0.13-lts/guides/monitoring.html](https://docs.bentoml.org/en/0.13-lts/guides/monitoring.html)

### 02 Structure 
Each element that you want to monitor is called a **metric**. 

The Prometheus server reads targets at an interval that you define to collect metrics and stores them in a **time series database**. 

You query the Prometheus time series database for where metrics are stored using the **PromQL query language**. The result of an expression can either be shown as a graph, viewed as tabular data in Prometheus's expression browser.

### 02 Key Elements
* **Prometheus Server** (the server which scrapes and stores the metrics data).
* **Targets** to be scraped, for example an instrumented application that exposes its metrics, or an exporter that exposes metrics of another application.
* **Exporters** are optional external programs that ingest data from a variety of sources and convert it to metrics that Prometheus can scrape. 
* **Alertmanager** to raise alerts based on preset rules.

<div align="center">
  <img width="650" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/prometheus_elements.png">
</div>

### 02 Guidelines

Alerting with Prometheus is separated into two parts:
* alerting rules in Prometheus servers send alerts to an Alertmanager,
* the Alertmanager (see afterwards)

## 03 Alert management

<div align="center">
  <img width="120" alt="alermanager logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/alermanager_logo.png">
</div>

:books: *Theory: To alert the data scientist of the change; that person can then diagnose the issue and evaluate the next course of action.*

[Alermanager](https://prometheus.io/docs/alerting/latest/overview/) manages the alerts and sending out notifications via methods such as email, slack, webhook, telegram.

It takes care of deduplicating, grouping, and routing them to the correct receiver integration. It also takes care of silencing and inhibition of alerts.

## 04 Managed observability platform

<div align="center">
  <img width="140" alt="grafana logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/grafana_logo.svg.png">
</div>

:books: *Theory: Model monitoring: The model predictive performance is monitored to potentially invoke a new iteration in the ML process.*

[Grafana](https://grafana.com/) provides a platform to visualizing in realt-time.

Grafana allows you to visualize monitoring metrics. It can visualize the results of monitoring work in the form of line graphs, heat maps, and histograms. 
You use Grafana GUI boards to request metrics from the Prometheus server and render them in the Grafana dashboard.

From this tool the users can create own dashboard with graphs personalized. Grafana dashboards are easy to setting and very flexible.
You can also save the dashboards  in json form to export.

## 05 Building application
<div align="center">
  <img width="260" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_logo.png">
</div>

[Streamlit](https://streamlit.io/) is an open-source Python library that facilitates building and deploying shareable web apps in minutes. It turns data scripts into customized, powerful, and shareable data apps. 

Being a production-ready app framework, Streamlit offers the fastest way to build web apps for machine learning models.

### 05 Structure
Adding a widget is the same as declaring a variable. No need to write a backend, define routes, handle HTTP requests, connect a frontend, write HTML, CSS, JavaScript, ...

### 05 Key Elements
When you're working with data, it is extremely valuable to visualize that data quickly, interactively, and from multiple different angles. 
You can display data via charts, and you can display it in raw form.
* Data display elements: DataFrame, Static tables, Metrics, Dicts and JSON.

<div align="center">
  <img width="680" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_data.png">
</div>

* Chart elements: Streamlit supports several different charting libraries as Matplotlib. And a few chart types that are "native" to Streamlit, like st.line_chart and st.area_chart

<div align="center">
  <img width="680" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/streamlit_chart.png">
</div>

# Bridge

## Interactions And Communication

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/comunications.png)

## Getting Started

To up and start docker images:
```
docker compose up
```
In Docker desktop appear these images: `prom/prometheus`, `grafana/grafana`, `mlops-observability-evidently_service`, `prom/alertmanager`. Also this command run `bento` image about the ml model.


To run the streamlit app:
```
streamlit run .\metrics_app\streamlit_app.py
```

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



In the next image you can see a example of an alert message sent to a chat Slack. Show a example of chat where Alertmanager send alert, with details.

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/chatSlack.png)

## Grafana Dashboard

![This is an image](https://github.com/giorgiaBertacchini/MLOps/blob/main/MLOps%20-observability/img_readme/grafana.png)


# Acknowledgments
