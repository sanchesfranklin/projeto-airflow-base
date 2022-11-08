import pandas as pd

url = "https://ptax.bcb.gov.br/ptax_internet/consultarTodasAsMoedas.do?method=consultaTodasMoedas"

def read_table():
    dataframe = pd.read_html(url, decimal=',', thousands='.')[0]

    print("Lendo tabela...")
    print(dataframe.tail())
    return dataframe


def save_csv():
    files = read_table()
    print(f"exportando arquivo...")
    files.to_csv("/opt/airflow/data/raw/cambio_moeda/currency.csv", index=False, encoding='utf-8')
    print(f"arquivo exportado")