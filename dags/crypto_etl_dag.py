from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')
from crypto_etl import extract_coin_data, load_to_postgres

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline for crypto prices',
    schedule_interval='@daily',
    catchup=False
)

def run_etl():
    df = extract_coin_data()
    load_to_postgres(df)

etl_task = PythonOperator(
    task_id='extract_transform_load_crypto_data',
    python_callable=run_etl,
    dag=dag
)

etl_task