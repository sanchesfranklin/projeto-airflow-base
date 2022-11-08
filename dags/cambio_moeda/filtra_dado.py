import pandas as pd
from datetime import date

def filtraCategoriaMoedas():
    data_atual = date.today()
    file = pd.read_csv(f'/opt/airflow/data/trusted/cambio_moeda/currency_transformed-{data_atual}.csv')
    
    df_filtrado = file.loc[file['TIPO'] == "A"]
    data_atual = date.today()
    # salvando em trusted
    file = df_filtrado
    file.to_csv(f"/opt/airflow/data/business/cambio_moeda/moedas_tipo_A-{data_atual}.csv", index=False, encoding='utf-8')