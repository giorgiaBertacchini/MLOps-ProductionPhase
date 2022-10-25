# MLOps - observability

## Run
```
docker compose up
```
In Docker desktop appear three images: `prom/prometheus`, `grafana/grafana`, `observability-evidently_service`.
```
python .\run_example.py
```

## Web

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

## Alerting

Alertmanager:
`localhost:9093`
