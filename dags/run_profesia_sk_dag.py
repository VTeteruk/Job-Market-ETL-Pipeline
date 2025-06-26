from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from scrapers.profesiaSK.main import main

default_args = {
    "owner": "Vlad",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    dag_id="run_profesia_sk",
    start_date=datetime(2025, 6, 19),
    catchup=True,
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="task_run_profesia_sk",
        python_callable=main
    )

    trigger_db_dag = TriggerDagRunOperator(
        task_id="trigger_db_dag",
        trigger_dag_id="db_dag",
        wait_for_completion=False,
        reset_dag_run=True,
        execution_date="{{ ds }}",
        dag=dag
    )

    task1 >> trigger_db_dag
