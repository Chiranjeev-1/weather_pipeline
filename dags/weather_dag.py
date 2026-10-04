from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os


# Tell Airflow where your pipeline files are
sys.path.insert(0, "/opt/airflow/pipeline")

from extract import extract_cities, extract_weather
from transform import transform
from load import load

default_args = {
    "owner": "chiranjeev",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False
}

def run_extract(**context):
    cities_df = extract_cities("/opt/airflow/pipeline/cities.csv")
    weather_df = extract_weather(cities_df)
    context["ti"].xcom_push(key="weather_data", value=weather_df.to_json())

def run_transform(**context):
    import pandas as pd
    raw_json = context["ti"].xcom_pull(key="weather_data", task_ids="extract")
    df = pd.read_json(raw_json)
    clean_df = transform(df)
    context["ti"].xcom_push(key="clean_data", value=clean_df.to_json())

def run_load(**context):
    import pandas as pd
    clean_json = context["ti"].xcom_pull(key="clean_data", task_ids="transform")
    df = pd.read_json(clean_json)
    load(df)

with DAG(
    dag_id="weather_etl_pipeline",
    default_args=default_args,
    description="Daily weather ETL pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "weather", "python"]
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=run_extract,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=run_transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=run_load,
        provide_context=True
    )

    extract_task >> transform_task >> load_task