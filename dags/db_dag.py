from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from plugins.data_cleaning import clean_data

default_args = {
    "owner": "Vlad",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}


def get_sql_from_file(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


with DAG(
    default_args=default_args,
    dag_id="db_dag",
    start_date=datetime(2025, 6, 19),
    catchup=True,
    schedule_interval="@daily"
) as dag:
    task1 = PostgresOperator(
        task_id="create_schemas",
        postgres_conn_id="local_postgres",
        sql=get_sql_from_file("/opt/airflow/project/database_initialization_scripts/init_db_schemas.sql")
    )

    task2 = PostgresOperator(
        task_id="create_bronze_table",
        postgres_conn_id="local_postgres",
        sql=get_sql_from_file("/opt/airflow/project/database_initialization_scripts/bronze_layer/init_table.sql")
    )

    task3 = PostgresOperator(
        task_id="from_csv_to_bronze",
        postgres_conn_id="local_postgres",
        sql=get_sql_from_file("/opt/airflow/project/database_initialization_scripts/bronze_layer/ingest_data.sql").replace(
            "<file_name>",
            "profesia_sk_jobs.csv"
        )
    )

    task4 = PostgresOperator(
        task_id="create_silver_table",
        postgres_conn_id="local_postgres",
        sql=get_sql_from_file("/opt/airflow/project/database_initialization_scripts/silver_layer/init_table.sql")
    )

    task5 = PythonOperator(
        task_id="from_bronze_to_silver",
        python_callable=clean_data
    )

    task1 >> task2 >> task3 >> task4 >> task5
