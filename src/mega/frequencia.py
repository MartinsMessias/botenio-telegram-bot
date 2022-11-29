"""Frequencia de números sorteados no Mega-Sena"""
import requests
import requests_cache
from lxml import etree
from bs4 import BeautifulSoup
from pprint import pprint

requests_cache.install_cache('req_cache', backend='sqlite', expire_after=180)

BASE_URL = 'https://www.somatematica.com.br/megasenaFrequentes.php'

def get_html(url):
    """Retorna o HTML da página"""
    response = requests.get(BASE_URL, timeout=5)
    soup = BeautifulSoup(response.content, 'html.parser')
    dom = etree.HTML(str(soup))
    return dom

def get_info():
    """Retorna informações sobre a página"""
    dom = get_html(BASE_URL)
    data_inicial = dom.xpath('//*[@id="content"]/section/p[2]/text()[2]')
    data_final = dom.xpath('//*[@id="content"]/section/p[2]/text()[3]')
    texto_topo = f'Nosso banco de dados abrange desde o concurso {data_inicial[0]}{data_final[0]}.'
    return texto_topo

def get_most_frequent():
    """Retorna os números mais frequentes"""
    dom = get_html(BASE_URL)
    most_frequent = []
    table = dom.xpath('//*[@id="sorteados"]/table')
    table = etree.tostring(table[0], pretty_print=True)
    table = BeautifulSoup(table, 'html.parser')
    table_rows = table.find_all('tr')
    table_rows = table_rows[2:]  # remove header row
    for row in table_rows:
        line = row.text.split()
        num = int(line[0])
        freq = int(line[2])
        most_frequent.append({num: freq})
    return most_frequent

def get_least_frequent():
    """Retorna os números menos frequentes"""
    dom = get_html(BASE_URL)
    least_frequent = []
    table = dom.xpath('//*[@id="atrasados"]/table')
    table = etree.tostring(table[0], pretty_print=True)
    table = BeautifulSoup(table, 'html.parser')
    table_rows = table.find_all('tr')
    table_rows = table_rows[1:]  # remove header row
    for row in table_rows:
        line = row.text.split()
        num = int(line[0])
        freq = int(line[4])
        least_frequent.append({num: freq})
    return least_frequent


def check_frequence(num):
    """Verifica a frequência de um número específico"""
    most_frequent = get_most_frequent()
    least_frequent = get_least_frequent()
    for item in most_frequent:
        if num in item:
            yield item[num]
    for item in least_frequent:
        if num in item:
            yield item[num]
    

def check_frequence_range(nums):
    """Verifica a frequência de um range de números"""
    freq = []
    for num in nums:
        r1, r2 = check_frequence(num)
        freq.append({num: r1})
    return freq
