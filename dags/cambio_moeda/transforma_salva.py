import pandas as pd
from datetime import date
import cambio_moeda.acessa_site as acessa


def getFile_currency():
    file = pd.read_csv('/opt/airflow/data/raw/cambio_moeda/currency.csv')
    return file

def transform():
    dataframe = getFile_currency()
    titulo_sites = acessa.getPage()

    dataframe = dataframe[dataframe.Tipo != 'Tipo']
    dataframe['Data'] = acessa.regex_dates(titulo_sites)
    dataframe_modificado = dataframe[['Data', 'Cod Moeda', 'Tipo', 'Moeda',
                                'Taxa Compra', 'Taxa Venda', 'Paridade Compra', 'Paridade Venda']]

    dataframe_modificado.rename(columns={
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

    data_atual = date.today()
    # salvando em trusted
    file = dataframe_modificado
    file.to_csv(f"/opt/airflow/data/trusted/cambio_moeda/currency_transformed-{data_atual}.csv", index=False, encoding='utf-8')