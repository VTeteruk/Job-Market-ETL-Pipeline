import pandas as pd
from pyspark.pandas import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, IntegerType, StringType, TimestampType, StructType
from airflow.providers.postgres.hooks.postgres import PostgresHook


def get_spark_session(app_name: str) -> SparkSession:
    return SparkSession.builder.appName(
        app_name
    ).config(
        "spark.executor.memory", "1g"
    ).config(
        "spark.driver.memory", "1g"
    ).config(
        "spark.sql.adaptive.enabled", "false"
    ).getOrCreate()


def get_db_data(spark) -> DataFrame:
    hook = PostgresHook(postgres_conn_id="local_postgres")
    df = hook.get_pandas_df(
        """
        SELECT
            job_id,
            url,
            source,
            title,
            company,
            location,
            job_type,
            workplace_type,
            experience_level,
            description,
            salary,
            posted_date,
            applicant_count,
            view_count
        FROM bronze.jobs
        """
    )

    if "posted_date" in df.columns:
        df["posted_date"] = pd.to_datetime(df["posted_date"])

    schema = StructType([
        StructField("job_id", IntegerType(), True),
        StructField("url", StringType(), True),
        StructField("source", StringType(), True),
        StructField("title", StringType(), True),
        StructField("company", StringType(), True),
        StructField("location", StringType(), True),
        StructField("job_type", StringType(), True),
        StructField("workplace_type", StringType(), True),
        StructField("experience_level", StringType(), True),
        StructField("description", StringType(), True),
        StructField("salary", StringType(), True),
        StructField("posted_date", TimestampType(), True),
        StructField("applicant_count", IntegerType(), True),
        StructField("view_count", IntegerType(), True),
    ])

    return spark.createDataFrame(df, schema=schema)


def save_to_db(df: DataFrame, _schema):
    hook = PostgresHook(postgres_conn_id="local_postgres")
    engine = hook.get_sqlalchemy_engine()
    pandas_df = df.toPandas()

    pandas_df.to_sql(
        name="jobs",
        con=engine,
        schema=_schema,
        if_exists="append",
        index=False
    )
