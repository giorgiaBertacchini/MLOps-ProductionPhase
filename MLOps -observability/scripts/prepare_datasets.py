import argparse
import io
import logging
import os
import shutil
import zipfile
from typing import Tuple

import pandas as pd
import requests



def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()]
    )


def get_data_bike_random_forest() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get bike dataset with random forest model prediction"""
    return get_data_bike(True)


def get_data_bike_gradient_boosting() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get bike dataset with gradient boosting model"""
    return get_data_bike(False)


def get_data_bike(use_model: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
    raw_data = pd.read_csv('model_input_table.csv', parse_dates=["dteday"])

    reference_bike_data = raw_data[:120]
    production_bike_data = raw_data[120:]

    target = "cnt"
    numerical_features = ["mnth", "temp", "atemp", "hum", "windspeed"]
    categorical_features = ["season", "holiday", "weekday", "workingday", "weathersit"]

    features = numerical_features + categorical_features

    if use_model:
        from sklearn.ensemble import RandomForestRegressor

        # get predictions with random forest
        model = RandomForestRegressor(random_state=0)

    else:
        from sklearn.ensemble import GradientBoostingRegressor

        model = GradientBoostingRegressor(random_state=0)

    model.fit(reference_bike_data[features], reference_bike_data[target])
    reference_bike_data["prediction"] = model.predict(reference_bike_data[features])
    production_bike_data["prediction"] = model.predict(production_bike_data[features])

    return reference_bike_data, production_bike_data


def main(dataset_name: str, dataset_path: str) -> None:
    logging.info("Generate test data for dataset %s", dataset_name)
    dataset_path = os.path.abspath(dataset_path)

    if os.path.exists(dataset_path):
        logging.info("Path %s already exists, remove it", dataset_path)
        shutil.rmtree(dataset_path)

    os.makedirs(dataset_path)

    reference_data, production_data = DATA_SOURCES[dataset_name]()
    logging.info("Save datasets to %s", dataset_path)
    reference_data.to_csv(os.path.join(dataset_path, "reference.csv"), index=False)
    production_data.to_csv(os.path.join(dataset_path, "production.csv"), index=False)

    logging.info("Reference dataset was created with %s rows", reference_data.shape[0])
    logging.info("Production dataset was created with %s rows", production_data.shape[0])


DATA_SOURCES = {
    "model_input_table": get_data_bike_random_forest,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    logging.info("run parser.add_argument")
    parser.add_argument(
        "-d",
        "--dataset",
        choices="model_input_table",
        type=str,
        help="Dataset name for reference.csv= and production.csv files generation.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path for saving dataset files.",
    )

    args = parser.parse_args()
    setup_logger()
    print(args)
    if args.dataset not in DATA_SOURCES:
        print(args)
        exit(f"Incorrect dataset name {args.dataset}, try to see correct names with --help")
    main(args.dataset, args.path)