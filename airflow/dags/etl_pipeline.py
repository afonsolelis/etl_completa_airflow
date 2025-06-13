from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
import os

# Adicionar o diretório ETL ao path
sys.path.append('/opt/airflow/etl')

# Configurações padrão da DAG
default_args = {
    'owner': 'dataops_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definição da DAG
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL completo de DataOps',
    schedule_interval=timedelta(hours=6),  # Executa a cada 6 horas
    catchup=False,
    tags=['dataops', 'etl', 'pipeline'],
)

def extract_database_data(**context):
    """Task para extração de dados do banco"""
    from extract.db_extractor import main as extract_db_main
    extract_db_main()

def extract_api_data(**context):
    """Task para extração de dados de APIs"""
    from extract.api_extractor import main as extract_api_main
    extract_api_main()

def transform_data(**context):
    """Task para transformação dos dados"""
    from transform.data_transformer import main as transform_main
    transform_main()

def load_data(**context):
    """Task para carregamento no data warehouse"""
    from load.data_loader import main as load_main
    load_main()

def validate_pipeline(**context):
    """Task para validação do pipeline"""
    import pandas as pd
    import json
    
    # Verificar se os arquivos foram criados
    required_files = [
        '/opt/airflow/data/raw/sales_data.csv',
        '/opt/airflow/data/processed/sales_clean.csv',
        '/opt/airflow/data/processed/data_quality_report.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        raise FileNotFoundError(f"Missing files: {missing_files}")
    
    # Verificar qualidade dos dados
    with open('/opt/airflow/data/processed/data_quality_report.json', 'r') as f:
        quality_report = json.load(f)
    
    for report in quality_report:
        if report['null_values'] > report['total_records'] * 0.1:  # Mais de 10% de nulos
            raise ValueError(f"Dataset {report['dataset']} has too many null values: {report['null_values']}")
    
    print("Pipeline validation successful!")

# Task 1: Criar diretórios necessários
create_directories = BashOperator(
    task_id='create_directories',
    bash_command='mkdir -p /opt/airflow/data/raw /opt/airflow/data/processed /opt/airflow/data/warehouse',
    dag=dag,
)

# Task 2: Extração de dados do banco de dados
extract_db_task = PythonOperator(
    task_id='extract_database_data',
    python_callable=extract_database_data,
    dag=dag,
)

# Task 3: Extração de dados de APIs
extract_api_task = PythonOperator(
    task_id='extract_api_data',
    python_callable=extract_api_data,
    dag=dag,
)

# Task 4: Transformação dos dados
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

# Task 5: Carregamento no data warehouse
load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Task 6: Validação do pipeline
validate_task = PythonOperator(
    task_id='validate_pipeline',
    python_callable=validate_pipeline,
    dag=dag,
)

# Task 7: Notificação de sucesso
notify_success = BashOperator(
    task_id='notify_success',
    bash_command='echo "Pipeline ETL executado com sucesso em $(date)"',
    dag=dag,
)

# Definindo dependências das tasks
create_directories >> [extract_db_task, extract_api_task]
[extract_db_task, extract_api_task] >> transform_task
transform_task >> load_task
load_task >> validate_task
validate_task >> notify_success