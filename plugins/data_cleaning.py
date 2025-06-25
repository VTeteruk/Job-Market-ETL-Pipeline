import pandas as pd
from pyspark.pandas import DataFrame
from pyspark.sql import SparkSession
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyspark.sql.functions import when, col, regexp_extract, regexp_replace, split, trim, initcap
from pyspark.sql.types import StructField, IntegerType, StringType, TimestampType, StructType


def get_spark_session() -> SparkSession:
    return SparkSession.builder.appName(
        "DataCleaning"
    ).config(
        "spark.executor.memory", "1g"
    ).config(
        "spark.driver.memory", "1g"
    ).config(
        "spark.sql.adaptive.enabled", "false"
    ).getOrCreate()


def get_db_data(spark) -> DataFrame:
    hook = PostgresHook(postgres_conn_id='local_postgres')
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

    if 'posted_date' in df.columns:
        df['posted_date'] = pd.to_datetime(df['posted_date'])

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


def save_to_db(df: DataFrame):
    hook = PostgresHook(postgres_conn_id='local_postgres')
    engine = hook.get_sqlalchemy_engine()
    pandas_df = df.toPandas()

    pandas_df.to_sql(
        name='jobs',
        con=engine,
        schema='silver',
        if_exists='append',
        index=False
    )


def clean_data():

    # TODO: ADD MORE CLEANING
    # TODO: SPLIT BY FUNCTIONS

    spark = get_spark_session()
    df = get_db_data(spark)

    df = df.withColumn(
        "location",
        when(col("location").contains(":"), None).otherwise(col("location"))
    )

    df = df.withColumn("salary_clean", regexp_replace(col("salary"), r"\s+", ""))

    df = df.withColumn("salary_amount", regexp_extract(col("salary_clean"), r"(\d+)", 1).cast("int"))

    df = df.withColumn("salary_no_digits", regexp_replace(col("salary_clean"), r"\d+", ""))

    df = df.withColumn("salary_parts", split(col("salary_no_digits"), "/"))

    df = df.withColumn("salary_currency", col("salary_parts").getItem(0))
    df = df.withColumn("salary_period", col("salary_parts").getItem(1))

    df = df.drop("salary", "salary_clean", "salary_no_digits", "salary_parts")

    df = df.withColumn(
        "description",
        trim(col("description"))
    )

    df = df.withColumn(
        "job_type",
        regexp_replace(initcap(col("job_type")), "_", " ")
    )

    df = df.withColumn(
        "workplace_type",
        regexp_replace(initcap(col("workplace_type")), "_", " ")
    )

    df = df.withColumn(
        "experience_level",
        regexp_replace(initcap(col("experience_level")), "_", " ")
    )

    df.show()

    save_to_db(df)
