from inspect import getfile
import requests
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import warnings
import time
from datetime import datetime,timedelta, date
import sqlalchemy

url = "https://ptax.bcb.gov.br/ptax_internet/consultarTodasAsMoedas.do?method=consultaTodasMoedas"

# Extraindo o dado/arquivo

def getPage():

    try:
        response = requests.get(url, timeout=30, verify=False)
    except requests.exceptions.RequestException:
        return None

    bs = BeautifulSoup(response.content, 'html.parser')
    titulo_site = [s.text for s in bs.find('div', {'align': 'center'}).find_all('strong')][0]

    return titulo_site

def regex_dates(titulo_site):
    try:
        match = re.search(r'(\d+/\d+/\d+)', titulo_site)
    except:
        match = None
    return match.group(1)

def read_table():
    dataframe = pd.read_html(url, decimal=',', thousands='.')[0]

    print("Lendo tabela...")
    print(dataframe.tail())
    return dataframe


def save_csv():
    files = read_table()
    print(f"exportando arquivo...")
    files.to_csv("/opt/airflow/dags/data/raw/cambio_moeda/currency.csv", index=False, encoding='utf-8')
    print(f"arquivo exportado")

# Caso precise salvar em .parquet, descomentar
# e alterar função chamada na task salva_arquivo
'''
def save_parquet():
    files = read_table()
    path = "/opt/airflow/dags/data/raw/cambio_moeda/"
    files.to_parquet(f"{path}currency.parquet", index=False)
    print(f"exportando arquivo parquet para {path}...")
'''

# Transformação

def getFile_currency():
    file = pd.read_csv('/opt/airflow/dags/data/raw/cambio_moeda/currency.csv')
    return file

def transform_dataframe():
    dataframe = getFile_currency()
    titulo_sites = getPage()

    dataframe_transformed = dataframe[dataframe.Tipo != 'Tipo']
    dataframe_transformed['Data'] = regex_dates(titulo_sites)
    dataframe_transformed2 = dataframe_transformed[['Data', 'Cod Moeda', 'Tipo', 'Moeda',
                                'Taxa Compra', 'Taxa Venda', 'Paridade Compra', 'Paridade Venda']]

    dataframe_transformed2.rename(columns={
        'Data': 'DATA',
        'Cod Moeda': 'COD_MOEDA',
        'Tipo': 'TIPO',
        'Moeda': 'MOEDA',
        'Taxa Compra': 'TAXA_COMPRA',
        'Taxa Venda': 'TAXA_VENDA',
        'Paridade Compra': 'PARIDADE_COMPRA',
        'Paridade Venda': 'PARIDADE_VENDA'
    }, inplace=True)

    print("Transformando a tabela...")
    #print(dataframe_transformed2.tail())

    data_atual = date.today()
    # salvando em trusted
    file = dataframe_transformed2
    file.to_csv(f"/opt/airflow/dags/data/trusted/cambio_moeda/currency_transformed-{data_atual}.csv", index=False, encoding='utf-8')
    #return dataframe_transformed2

'''
def save_csv_transformed():
    data_atual = date.today()
    file = transform_dataframe()
    file.to_csv(f"/opt/airflow/dags/data/trusted/currency_transformed-{data_atual}.csv", index=False, encoding='utf-8')
    print("arquivo exportado")
'''

# Business
def filtraCategoriaMoedas():
    data_atual = date.today()
    file = pd.read_csv(f'/opt/airflow/dags/data/trusted/cambio_moeda/currency_transformed-{data_atual}.csv')
    
    df_filtrado = file.loc[file['TIPO'] == "A"]
    data_atual = date.today()
    # salvando em trusted
    file = df_filtrado
    file.to_csv(f"/opt/airflow/dags/data/business/moedas_tipo_A-{data_atual}.csv", index=False, encoding='utf-8')

# Carga
def load_olap():
    print('teste')
    # conectando com o banco postgresql
    engine_postgresql_olap = sqlalchemy.create_engine('postgresql+psycopg2://postgres:airflow@172.19.0.8:5460/moedas')

    data_atual = date.today()
    # capturar os dados do arquivo
    df_dados = pd.read_csv(f'/opt/airflow/dags/data/business/moedas_tipo_A-{data_atual}.csv')
    # carregando os dados para o banco de dados
    df_dados.to_sql("moedas_dataset", engine_postgresql_olap, if_exists="append", index=False)
