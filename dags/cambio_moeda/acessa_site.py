import requests
from requests import get
from bs4 import BeautifulSoup
import re

url = "https://ptax.bcb.gov.br/ptax_internet/consultarTodasAsMoedas.do?method=consultaTodasMoedas"

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