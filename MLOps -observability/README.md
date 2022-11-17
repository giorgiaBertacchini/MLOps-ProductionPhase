<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img width="200" alt="logo" src="https://github.com/giorgiaBertacchini/MLOps-DevelopPhase/blob/main/img_readme/logo.png">
  <h1 align="center">MLOps</h1>
  <h3 align="center">To automate and encourage machine learning in enterprises!</h3>
</div>

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
          <li><a href="#01-guidelines">01 Guidelines</a></li>
        </ul>
        <li><a href="#02-systems-monitoring-and-alerting">02 Systems monitoring and alerting</a></li>        
        <ul>
          <li><a href="#02-collaboration">02 Collaboration</a></li>
          <li><a href="#02-structure">02 Structure</a></li>
          <li><a href="#02-key-elements">02 Key Elements</a></li>
          <li><a href="#02-guidelines">02 Guidelines</a></li>
        </ul>
        <li><a href="#03-alert-management">03 Alert management</a></li>
        <ul>
          <li><a href="#03-guidelines">02 Guidelines</a></li>
        </ul>
        <li><a href="#04-managed-observability-platform">04 Managed observability platform</a></li>
        <ul>
          <li><a href="#04-guidelines">02 Guidelines</a></li>
        </ul>
        <li><a href="#05-building-application">05 Building application</a></li>
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
  <img width="700" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/mon_tools.png">
</div>

| Tool | Port |
| --- | --- |
| Bento | `localhost:3005` |
| Service | `localhost:8085` |
| Prometheus | `localhost:9090` |
| Alertmanager | `localhost:9093` |
| Grafana | `localhost:3000` |
| Streamlit App | `localhost:8501` |

## Schema

<div align="center">
  <img width="700" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/schema.png">
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
  <img width="300" alt="evidently logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/evidently_logo.png">
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

[Real-time ML monitoring with Evidently and Grafana](https://github.com/evidentlyai/evidently/tree/main/examples/integrations/grafana_monitoring_service)

<div align="center">
  <img width="650" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/integration.png">
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

### 01 Guidelines

Evidently needs to be installed:
```
pip install evidently
```

#### Evidently Monitors
`metrics_app/app.py` implements evidently monitors and the integration with Prometheus. 

``` python
from evidently.model_monitoring import CatTargetDriftMonitor
from evidently.model_monitoring import ClassificationPerformanceMonitor
from evidently.model_monitoring import DataDriftMonitor
from evidently.model_monitoring import DataQualityMonitor
from evidently.model_monitoring import ModelMonitoring
from evidently.model_monitoring import NumTargetDriftMonitor
from evidently.model_monitoring import ProbClassificationPerformanceMonitor
from evidently.model_monitoring import RegressionPerformanceMonitor
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.runner.loader import DataLoader

EVIDENTLY_MONITORS_MAPPING = {
    "cat_target_drift": CatTargetDriftMonitor,
    "data_drift": DataDriftMonitor,
    "data_quality": DataQualityMonitor,
    "num_target_drift": NumTargetDriftMonitor,
    "regression_performance": RegressionPerformanceMonitor,
    "classification_performance": ClassificationPerformanceMonitor,
    "prob_classification_performance": ProbClassificationPerformanceMonitor,
}
```

#### Evidently Reports And Tests

`scripts/monitoring.py` file implement Evidently tool without the integration with Prometheus and Granafa. So it is not real-time observation and create in output html pages. These output are saved in `metrics_app/templates` folder. If these pages will be usefull can be exported for extern uses.

*Importing*
``` python
from evidently.report import Report
from evidently.metric_preset import DataDrift, NumTargetDrift
 
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStability
from evidently.tests import *
```

*Data Stability*
``` python
def data_stability_test(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("Data stability test. Test suite.")
     # A test suite contains several individual tests. Each test compares a specific metric against a defined condition and returns a pass/fail result. 
    # DataStability run several checks for data quality and integrity

    data_stability = TestSuite(tests=[DataStability(),])
    data_stability.run(reference_data=reference, current_data=current)
    data_stability.save_html(os.path.join("metrics_app", "templates", "data_stability.html"))
```

*Report*
``` python
def drift_report(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("DataDrift and NumTargetDrift. Drift report.")
    # Reports calculate various metrics and generate a dashboard with rich visuals.

    drift_report = Report(metrics=[DataDrift(), NumTargetDrift()])
    drift_report.run(reference_data=reference, current_data=current)
    drift_report.save_html(os.path.join("metrics_app", "templates", "drift_report.html"))
```

*Test Suite*
``` python
def data_tests(reference: pd.DataFrame, current: pd.DataFrame):
    logging.info("DataDrift and NumTargetDrift. Drift report.")
    # Data drift and feature drift

    data_drift_tests = TestSuite(tests=[
        TestNumberOfColumnsWithNulls(),
        TestNumberOfRowsWithNulls(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestNumberOfDriftedFeatures(),
        TestShareOfDriftedFeatures(),
    ])
    data_drift_tests.run(reference_data=reference, current_data=current)
    data_drift_tests.save_html(os.path.join("metrics_app", "templates", "data_drift_tests.html"))
```

Example of created html pages:

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/drift_html.png)
![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/report_html.png)

## 02 Systems monitoring and alerting
<div align="center">
  <img width="300" alt="prometheus logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/prometheus_logo.png">
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
  <img width="650" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/prometheus_elements.png">
</div>

### 02 Guidelines

`config/prometheus.yml` file with Prometheus configuration. For example with rules source, the alerting destination, and all service that it monitoring.

``` yaml
# Load and evaluate rules in this file every 'evaluation_interval' seconds.
rule_files:
  - "prometheus_rules.yml"

alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: [ 'alertmanager:9093' ]

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s
    static_configs:
         - targets: ['localhost:9090']

  - job_name: 'service'
    scrape_interval: 10s
    static_configs:
      - targets: ['evidently_service.:8085']

  - job_name: 'bentoml'
    scrape_interval: 10s
    static_configs:
      - targets: ['bentoml.:3005']

  - job_name: 'alertmanager'
    scrape_interval: 10s
    static_configs:
      - targets: ['alertmanager.:9093']
```

`metrics_app/app.py`

``` python
import prometheus_client

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": prometheus_client.make_wsgi_app()})
```
``` python
class MonitoringService:
    # names of monitoring datasets
    datasets: LoadedDataset
    metric: prometheus_client.Gauge
```

Alerting with Prometheus is separated into two parts:
* alerting rules in Prometheus servers send alerts to an Alertmanager,
* the Alertmanager (see afterwards)

`config/prometheus_rules.yml` file contains all alert rules with they Prometheus generate alerts. Following an example rule in the code.

``` yaml
- name: alert_rules
  rules:  
      - alert: FeaturesDrift
        expr: evidently:data_drift:n_drifted_features > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Features drifting from (instance {{ $labels.instance }})"
          description: "The number of feature drifted is {{ $value }}"
```

## 03 Alert management

<div align="center">
  <img width="120" alt="alermanager logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/alermanager_logo.png">
</div>

:books: *Theory: To alert the data scientist of the change; that person can then diagnose the issue and evaluate the next course of action.*

[Alermanager](https://prometheus.io/docs/alerting/latest/overview/) manages the alerts and sending out notifications via methods such as email, slack, webhook, telegram.

It takes care of deduplicating, grouping, and routing them to the correct receiver integration. It also takes care of silencing and inhibition of alerts.

### 03 Guidelines
`config/alertmanager.yml` is where is specified the destination of notifications. In this case is a Slack channel. It contains also the format message sended, throught *title* and *text*.

``` yaml
route:
  group_by: [ alertname  ]
  receiver: slack_notifications
receivers:   
    - name: slack_notifications
      slack_configs:
      - api_url: 'https://hooks.slack.com/services/****'
        channel: '#monitoring'
        send_resolved: true
        icon_url: https://avatars3.githubusercontent.com/u/3380462
        title: |-
          [{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonLabels.alertname }} for {{ .CommonLabels.job }}
          {{- if gt (len .CommonLabels) (len .GroupLabels) -}}
            {{" "}}(
            {{- with .CommonLabels.Remove .GroupLabels.Names }}
              {{- range $index, $label := .SortedPairs -}}
                {{ if $index }}, {{ end }}
                {{- $label.Name }}="{{ $label.Value -}}"
              {{- end }}
            {{- end -}}
            )
          {{- end }}
        text: >-
          {{ range .Alerts -}}
          *Alert:* {{ .Annotations.title }}{{ if .Labels.severity }} - `{{ .Labels.severity }}`{{ end }}
          *Description:* {{ .Annotations.description }}
          *Details:*
            {{ range .Labels.SortedPairs }} • *{{ .Name }}:* `{{ .Value }}`
            {{ end }}
          {{ end }}
```

## 04 Managed observability platform

<div align="center">
  <img width="140" alt="grafana logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/grafana_logo.svg.png">
</div>

:books: *Theory: Model monitoring: The model predictive performance is monitored to potentially invoke a new iteration in the ML process.*

[Grafana](https://grafana.com/) provides a platform to visualizing in realt-time.

Grafana allows you to visualize monitoring metrics. It can visualize the results of monitoring work in the form of line graphs, heat maps, and histograms. 
You use Grafana GUI boards to request metrics from the Prometheus server and render them in the Grafana dashboard.

From this tool the users can create own dashboard with graphs personalized. Grafana dashboards are easy to setting and very flexible.
You can also save the dashboards  in json form to export.


### 04 Guidelines
`config/grafana_datasource.yaml` file contain the data sources to show in its dashboard.

``` yaml
# list of datasources that should be deleted from the database
deleteDatasources:
  - name: Prometheus
    orgId: 1

# list of datasources to insert/update depending
# what's available in the database
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus.:9090
```

## 05 Building application
<div align="center">
  <img width="260" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_logo.png">
</div>

:books: *Theory: A drift alert can be followed by a trigger to the Develop phase to retrain and generate a new model.* 

[Streamlit](https://streamlit.io/) is an open-source Python library that facilitates building and deploying shareable web apps in minutes. It turns data scripts into customized, powerful, and shareable data apps. 

Being a production-ready app framework, Streamlit offers the fastest way to build web apps for machine learning models.

### 05 Structure
Adding a widget is the same as declaring a variable. No need to write a backend, define routes, handle HTTP requests, connect a frontend, write HTML, CSS, JavaScript, ...

### 05 Key Elements
When you're working with data, it is extremely valuable to visualize that data quickly, interactively, and from multiple different angles. 
You can display data via charts, and you can display it in raw form.
* Data display elements: DataFrame, Static tables, Metrics, Dicts and JSON.

<div align="center">
  <img width="680" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_data.png">
</div>

* Chart elements: Streamlit supports several different charting libraries as Matplotlib. And a few chart types that are "native" to Streamlit, like st.line_chart and st.area_chart

<div align="center">
  <img width="680" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_chart.png">
</div>

### 05 Guidelines
streamlit requires installation:
```
pip install streamlit
```

# Bridge

## Interactions And Communication

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/comunications.png)

## Getting Started

To run the streamlit app:
```
streamlit run .\metrics_app\streamlit_app.py
```

To up and start docker images:
```
docker compose up
```
In Docker desktop appear/run these images: `prom/prometheus`, `grafana/grafana`, `mlops-observability-evidently_service`, `prom/alertmanager`. Also this command run `bento` image about the ml model. You can see the details in `docker-compose.yml`.
``` python
services:
  evidently_service:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8085:8085"
    [...]

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    [...]

  grafana:
    image: grafana/grafana
    user: "472"
    depends_on:
      - prometheus
    ports:
      - "3000:3000"
    [...]

  bentoml:
    image: activities_model:${TAG}
    ports:
      - "3005:3005"
    [...]

  alertmanager:
    image: prom/alertmanager:v0.23.0
    ports:
      - "9093:9093"
    [...]
```
*Note: in bentoml image is used {TAG}, so it run the latest ml model.*

### First time
But for the first time, before:
1. you need to update TAG as environment variable, to have the latest built model.
    * From streamlit app, in the fourth tab "Single actinos" there is the button "Update model in monitoring sector?" to update the model that is the TAG.
2. you need to specify your destination of notifications.
    * In `config/alermanager.yml` file:
      ``` yaml
      slack_configs:
      - api_url: ****
        channel: '#monitoring'
      ```
      
### Parameters
For change the parameters, there is `parameters/params.json`.
Instead `parameters/header_params.json` is automatically update with the header params of Develop Phase.

## Prerequisites

## Installation

The installations are execute through `Dockerfile`:
``` python
RUN pip3 install -r requirements.txt
```

To run streamlit app. it is necessary:
```
pip install streamlit
```

# Usage

## Streamlit App

From this application the users can:

- require predictions,

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_Predictions.png)

- find directly link to observation tools,

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_Monitor.png)

- run to retrain the ml model or run single actions usefull.

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/streamlit_CompleteRetrain.png)

## Prometheus Dashboard
![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/prometheus.png)

From its `/alerts` the user can see the alert active and which is verified.

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/prometheus_alert.png)

## AlertManager Dashboard

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/alertmanager.png)

In the next image you can see a example of an alert message sent to a chat Slack. Show a example of chat where Alertmanager send alert, with details.

<div align="center">
  <img width="800" alt="streamlit logo" src="https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/chatSlack.png">
</div>

## Grafana Dashboard

![This is an image](https://github.com/giorgiaBertacchini/MLOps-ProductionPhase-Slide/blob/main/MLOps%20-observability/img_readme/grafana.png)

# Acknowledgments
* [mlebook, chapter 9](https://www.dropbox.com/s/yix71gdh445b6j0/Chapter9.pdf?dl=0)
* [Made With ML](https://madewithml.com/courses/mlops/monitoring/)
* Book "Introducing MLOps How to Scale Machine Learning in the Enterprise (Mark Treveil, Nicolas Omont, Clément Stenac etc.)", Chapter 7
