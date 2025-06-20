from datetime import timedelta, datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    "owner": "Vlad",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    dag_id="db_dag",
    start_date=datetime(2025, 6, 19),
    catchup=True,
    schedule_interval="@daily"
) as dag:

    # TODO: MOVE TO SETTINGS / SPLIT BY FUNCTIONS:
    with open("/opt/airflow/project/database_initialization_scripts/init_db_schemas.sql", "r") as file:
        init_schema_sql = file.read()

    task1 = PostgresOperator(
        task_id="create_schemas",
        postgres_conn_id="local_postgres",
        sql=init_schema_sql  # ✅ now a raw SQL string, not a template path
    )

    with open("/opt/airflow/project/database_initialization_scripts/bronze_layer/init_table.sql", "r") as file:
        init_bronze_layer_sql = file.read()

    task2 = PostgresOperator(
        task_id="create_bronze_table",
        postgres_conn_id="local_postgres",
        sql=init_bronze_layer_sql
    )

    task1 >> task2
