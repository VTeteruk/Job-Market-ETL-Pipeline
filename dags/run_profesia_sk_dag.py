import os
import sys
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapers.profesiaSK.main import main

default_args = {
    "owner": "Vlad",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    dag_id="run_profesia_sk_v2",
    start_date=datetime(2025, 6, 19),
    catchup=True,
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="task_run_profesia_sk",
        python_callable=main
    )

    task1
