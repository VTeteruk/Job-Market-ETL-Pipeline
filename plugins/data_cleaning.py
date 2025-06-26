from airflow.providers.postgres.hooks.postgres import PostgresHook
from pyspark.pandas import DataFrame
from pyspark.sql.functions import when, col, regexp_extract, regexp_replace, split, trim, initcap, lower

from plugins.config import get_spark_session, get_db_data, save_to_db


def split_salary(df: DataFrame) -> DataFrame:
    df = df.withColumn("salary_clean", regexp_replace(col("salary"), r"\s+", ""))

    df = df.withColumn("salary_amount", regexp_extract(col("salary_clean"), r"(\d+)", 1).cast("int"))

    df = df.withColumn("salary_no_digits", regexp_replace(col("salary_clean"), r"\d+", ""))

    df = df.withColumn("salary_parts", split(col("salary_no_digits"), "/"))

    df = df.withColumn("salary_currency", col("salary_parts").getItem(0))
    df = df.withColumn("salary_period", col("salary_parts").getItem(1))

    return df.drop("salary", "salary_clean", "salary_no_digits", "salary_parts")


def clean_location(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "location",
        when(col("location").contains(":"), None).otherwise(col("location"))
    )


def clean_description(df: DataFrame) -> DataFrame:
    df = df.withColumn(
        "description",
        trim(regexp_replace(col("description"), "\n", " "))
    )

    return df.withColumn(
        "description",
        regexp_replace(col("description"), "Job description, responsibilities and duties ", "")
    )


def delete_underscores(df: DataFrame) -> DataFrame:
    df = df.withColumn(
        "job_type",
        initcap(regexp_replace(col("job_type"), "_", " "))
    )

    df = df.withColumn(
        "workplace_type",
        initcap(regexp_replace(col("workplace_type"), "_", " "))
    )

    return df.withColumn(
        "experience_level",
        initcap(regexp_replace(col("experience_level"), "_", " "))
    )


def translate_salary_period(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "salary_period",
        when(lower(col("salary_period")) == "mesiac", "month")
        .when(lower(col("salary_period")) == "měsíc", "month")
        .when(lower(col("salary_period")) == "monat", "month")
        .when(lower(col("salary_period")) == "hod.", "hour")
        .otherwise(col("salary_period"))
    )


def handle_nulls(df: DataFrame) -> DataFrame:
    return df.fillna({
        "location": "n/a",
        "job_type": "n/a",
        "workplace_type": "n/a",
        "experience_level": "n/a",
        "salary_currency": "n/a",
        "salary_period": "n/a",
        "company": "n/a",
        "description": "n/a",
        "applicant_count": 0,
        "view_count": 0,
    })


def clean_data():
    spark = get_spark_session("DataCleaning")
    df = get_db_data(spark)

    df = split_salary(df)
    df = clean_location(df)
    df = clean_description(df)
    df = delete_underscores(df)
    df = handle_nulls(df)

    df = translate_salary_period(df)

    save_to_db(df, "silver")
