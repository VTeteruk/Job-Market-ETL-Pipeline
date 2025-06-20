import os.path
import sys
from datetime import timedelta, datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

default_args = {
    "owner": "Vlad",
    "retries": 2,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    dag_id="db_tables_init_v1",
    start_date=datetime(2025, 6, 19),
    catchup=True,
    schedule_interval="@daily"
) as dag:
    task1 = PostgresOperator(
        task_id="create_schemas",
        postgres_conn_id="local_postgres",
        # TODO: IMPORT
        sql="""
        CREATE SCHEMA IF NOT EXISTS bronze;
        CREATE SCHEMA IF NOT EXISTS silver;
        CREATE SCHEMA IF NOT EXISTS gold;
        """
    )

    task2 = PostgresOperator(
        task_id="create_bronze_table",
        postgres_conn_id="local_postgres",
        # TODO: IMPORT
        sql="""
        /*
=====================================================
Job Market ETL Pipeline - Bronze Layer Table Setup
=====================================================
Purpose: Creates the bronze.jobs table for storing raw job data from multiple sources
Layer: Bronze (raw data ingestion layer)
Sources: Job platforms
=====================================================
*/

DROP TABLE IF EXISTS bronze.jobs;

CREATE TABLE bronze.jobs (
	job_id BIGINT PRIMARY KEY,
	url VARCHAR(255) NOT NULL,
	source VARCHAR(255) NOT NULL,
	title VARCHAR(255),
	company VARCHAR(255),
	location VARCHAR(255),
	job_type VARCHAR(255),
	workplace_type VARCHAR(255),
	experience_level VARCHAR(255),
	description TEXT,
	salary VARCHAR(50),
	posted_date DATE,
	applicant_count INT,
	view_count INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """
    )

    task1 >> task2
