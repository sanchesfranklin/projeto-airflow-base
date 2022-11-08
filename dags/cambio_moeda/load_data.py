import pandas as pd
from datetime import date
import sqlalchemy


def load_olap():
    print('teste')
    # conectando com o banco postgresql
    engine_postgresql_olap = sqlalchemy.create_engine('postgresql+psycopg2://postgres:airflow@172.19.0.8:5460/moedas')

    data_atual = date.today()
    # capturar os dados do arquivo
    df_dados = pd.read_csv(f'/opt/airflow/data/business/moedas_tipo_A-{data_atual}.csv')
    # carregando os dados para o banco de dados
    df_dados.to_sql("moedas_dataset", engine_postgresql_olap, if_exists="append", index=False)