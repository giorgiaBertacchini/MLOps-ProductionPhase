import argparse
import logging
import os
import shutil
import subprocess

import pandas as pd

def setup_logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()]
    )


def check_docker_installation():
    logging.info("Check docker version")
    docker_version_result = os.system("docker -v")

    if docker_version_result:
        exit("Docker was not found. Try to install it with https://www.docker.com")


def check_dataset(
    force: bool,
    datasets_path: str,
    dataset_name: str,
) -> None:
    logging.info("Check dataset %s", dataset_name)
    dataset_path = os.path.join(datasets_path, dataset_name)

    if os.path.exists(dataset_path):
        if force:
            logging.info("Remove dataset directory %s", dataset_path)
            shutil.rmtree(dataset_path)
            os.makedirs(dataset_path)

        else:
            logging.info("Dataset %s already exists", dataset_name)
            return

    logging.info("Download dataset %s", dataset_name)
    #run_script(cmd=["scripts/prepare_datasets.py"], wait=True)


def download_test_datasets(force: bool):
    datasets_path = os.path.abspath("datasets")
    logging.info("Check datasets directory %s", datasets_path)

    if not os.path.exists(datasets_path):
        logging.info("Create datasets directory %s", datasets_path)
        os.makedirs(datasets_path)

    else:
        logging.info("Datasets directory already exists")

    dataset_name = "model_input_table"
    check_dataset(force, datasets_path, dataset_name)


def run_docker_compose():
    logging.info("Run docker compose")
    run_script(cmd=["docker", "compose", "up", "-d"], wait=True)


def run_script(cmd: list, wait: bool) -> None:
    logging.info("Run %s", " ".join(cmd))
    script_process = subprocess.Popen(" ".join(cmd) , stdout=subprocess.PIPE, shell=True)

    if wait:
        script_process.wait()

        if script_process.returncode != 0:
            exit(script_process.returncode)


def send_data_requests():
    logging.info("Run scripts/example_run_request.py")
    os.system("python scripts/example_run_request.py")


def run_monitoring_html():
    logging.info("Run metrics_app/monitoring.py")
    os.system("python metrics_app/monitoring.py")

def stop_docker_compose():
    logging.info("Run docker compose down")
    os.system("docker compose down")

def run_streamlit():
    logging.info("Run streamlit")
    os.system("streamlit run streamlit_app.py")


def main(force: bool):
    setup_logger()
    check_docker_installation()
    download_test_datasets(force=force)
    run_docker_compose()
    send_data_requests()
    run_monitoring_html()
    run_streamlit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Remove and download again test datasets",
    )
    parameters = parser.parse_args()
    main(force=parameters.force)