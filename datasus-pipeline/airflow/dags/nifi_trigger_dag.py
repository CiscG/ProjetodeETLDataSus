from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'pessoal4',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='trigger_nifi_datasus_extraction',
    default_args=default_args,
    description='Orquestra a extração de CSVs do DATASUS via Apache NiFi',
    schedule_interval='0 12 * * *', # Executa diariamente às 12:00
    start_date=datetime(2026, 5, 1),
    catchup=False,
    tags=['datasus', 'nifi', 'raw_data'],
) as dag:

    # Envia o comando via API REST para o NiFi iniciar o script Python
    trigger_nifi = SimpleHttpOperator(
        task_id='call_nifi_api',
        http_conn_id='nifi_default',
        endpoint='contentListener',
        method='POST',
        data='{"action": "start_extraction", "source": "csv_datasus"}',
        headers={"Content-Type": "application/json"},
        log_response=True
    )
