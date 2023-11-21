import requests
import re
from bs4 import BeautifulSoup
from datetime import date

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

def find_by_label(soup, tag, label_list):
    for label in label_list:
        item = soup.find(f"{tag}", string=re.compile(label))
        if item is not None:
            return item.next_sibling
    return "Não informado"

def find_by_label_twice(soup, tag, label_list):
    for label in label_list:
        item = soup.find(f"{tag}", string=re.compile(label))
        if item is not None:
            return item.next_sibling.next_sibling.text
    return "Não informado"

def busca_padrao(link_vereadores, a_class):

    lista_vereadores = dict()
    lista_links = []
    requisicao = requests.get(link_vereadores, headers=headers)
    siteLinks = BeautifulSoup(requisicao.text, "html.parser")
    for a in siteLinks.find_all('a', class_=a_class):
        lista_links.append(a['href'])
    
    for link in lista_links:
        requisicao = requests.get(link, headers=headers)
        site = BeautifulSoup(requisicao.text, "html.parser")
        vereador = dict()
        nome = find_by_label(site, "strong", ["Nome Completo: "]).strip()
        print(nome)
        vereador["partido"] = find_by_label(site, "strong", ["Partido: "]).strip()
        vereador["data_nascimento"] = find_by_label(site, "strong", ["Nascimento: "]).strip()
        vereador["estado_civil"] = find_by_label(site, "strong", ["Estado Civil: "]).strip()
        vereador["escolaridade"] = find_by_label(site, "strong", ["Grau de Instrução: "]).strip()
        vereador["email"] = find_by_label(site, "strong", ["E-mail: "]).strip()
        vereador["telefone"] = find_by_label(site, "strong", ["Telefone: ", "Celular: "]).strip()

        lista_vereadores[nome] = vereador
    
    return lista_vereadores

def busca_alternativa(link_vereadores, link_individual):

    lista_vereadores = dict()
    lista_links = []
    requisicao = requests.get(link_vereadores, headers=headers)
    site = BeautifulSoup(requisicao.text, "html.parser")
    for a in site.find_all('a', class_="list-link"):
        lista_links.append(a['href'])
    lista_ordenada_partidos = site.find_all('p', class_="vereador-desc")
    i = 0
    for a in site.find_all('strong', class_="vereador-nome"):
        lista_vereadores[a.text] = dict()
        lista_vereadores[a.text]["partido"] = lista_ordenada_partidos[i].text.split("                                                                                    ")[1]

    for link in lista_links:
        link = f"{link_individual}{link}"
        requisicao = requests.get(link, headers=headers)
        site = BeautifulSoup(requisicao.text, "html.parser")

        nome = site.find("h1", class_="vereador-nome").text.split("                \t")[1]
        print(nome)
        data_nascimento = find_by_label_twice(site, "strong", ["Nascimento"])
        if data_nascimento != "Não informado":
            lista_vereadores[nome]["data_nascimento"] = data_nascimento.split("                            ")[1][:-24]
        else:
            lista_vereadores[nome]["data_nascimento"] = data_nascimento
        lista_vereadores[nome]["estado_civil"] = find_by_label_twice(site, "strong", ["Estado Civil"])
        lista_vereadores[nome]["escolaridade"] = find_by_label_twice(site, "strong", ["Escolaridade"])
        email = find_by_label_twice(site, "strong", ["E-mail"])
        if email != "Não informado":
            lista_vereadores[nome]["email"] = email.split("                            ")[1][:-24]
        else:
            lista_vereadores[nome]["email"] = email
        lista_vereadores[nome]["telefone"] = find_by_label_twice(site, "strong", ["Telefones"])
    
    return lista_vereadores

def calculate_age(b_date):
    current_date = date.today()
    birth_date = date(int(b_date[2]), int(b_date[1]), int(b_date[0]))
    years = current_date.year - birth_date.year
    months = current_date.month - birth_date.month
    days = current_date.day - birth_date.day

    if days < 0:
        months -= 1
        days += get_days_in_month(birth_date.month, birth_date.year)
    if months < 0:
        years -= 1
        months += 12

    return years

def get_days_in_month(month, year):
    if month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): 
            return 29
        else:
            return 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31