from airflow import DAG
import airflow.utils.dates
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from time import perf_counter

# refatorado funções
#from acessa_site import getPage
import cambio_moeda.acessa_site as acessa
import cambio_moeda.salva_arquivo as save
import cambio_moeda.transforma_salva as transform
import cambio_moeda.filtra_dado as filtra
import cambio_moeda.load_data as load

# email de notificação
email = "sanchesgabriellu@gmail.com"

#configuração da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 10, 30),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    # Execute uma vez a cada 15 minutos 
    # 'schedule_interval': '*/2 * * * *'
    'schedule_interval': None

}

with DAG(dag_id='moedas', 
        default_args=default_args, 
        schedule_interval=None,
        tags=['currency']
        ) as dag:
    
    # acessa o site
    acessa_site = PythonOperator(
        task_id='acessa_site',
        python_callable= acessa.getPage,
        do_xcom_push = False,
        dag=dag,    
    )

    # salvar arquivo csv em raw
    salva_arquivo = PythonOperator(
        task_id='salva_arquivo',
        python_callable= save.save_csv,
        do_xcom_push = False,
        dag=dag,
    )

    # transformando o arquivo - ajustando nomes tabelas e salvando (trusted).
    transforma_dado = PythonOperator(
        task_id='transforma_salva',
        python_callable= transform.transform,
        do_xcom_push = False,
        dag=dag,
    )

    # Aplica uma regra de negócio e salva em business
    filtra_dado = PythonOperator(
        task_id='filtra_dado',
        python_callable= filtra.filtraCategoriaMoedas,
        do_xcom_push = False,
        dag=dag,
    )

    # Carrega os dados no banco de dados
    load_data = PythonOperator(
        task_id = "load_data",
        email_on_failure = True,
        email = email,
        python_callable= load.load_olap,
        dag=dag,
    )

    # Task para enviar email de conclusão da pipe
    email_send = EmailOperator(
        task_id = "notificacao",
        to = email,
        subject= 'Pipeline Finalizado',
        html_content='<p> Pipeline para extração de moedas para ambiente OLAP finalizado!</p>',
        dag=dag
    )
    
    
    #dependências entre as tarefas
    acessa_site >> salva_arquivo >> transforma_dado >> filtra_dado >> load_data >> email_send
