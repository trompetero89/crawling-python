import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import time


# Función para extraer links dada una url
def extract_links(url, nivel):
    # time.sleep(3)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    # busca los enlaces de interés en este ccaso los que contienen la cadena 'facultades'
    if nivel == 1:
        for tag in soup.find_all('a', {'href': re.compile('facultades|administrativo\/')}):
            newurl = tag['href']
            # en caso de que haya url's relativas
            if newurl.startswith('/'):
                newurl = urljoin(url, newurl)
                links.append(newurl)
            if newurl.startswith('http'):
                links.append(newurl)
            print(newurl)
        # Devuelve una lista de links sin duplicados
        links = list(set(links))
        return links
    # busca los enlaces de los departamentos
    if nivel == 2:
        for tag in soup.find_all('div', class_='views-field views-field-field-url-caja-list1'):
            newurl = tag.a['href']
            links.append(newurl)
        return links
    if nivel == 3:
        for tag in soup.find_all('a', {'href': re.compile('index\.php\/el-departamento')}):
            newurl = tag['href']
            if newurl.startswith('/'):
                newurl = urljoin(url, newurl)
                links.append(newurl)
            if newurl.startswith('http'):
                links.append(newurl)
        links = list(set(links))
        return links
    if nivel == 4:
        for tag in soup.find_all('a', {'href': re.compile('(profesores|equipo|noticias-y-eventos.\w|noticias)')}):
            newurl = tag['href']
            if newurl.startswith('/'):
                newurl = urljoin(url, newurl)
                links.append(newurl)
            if newurl.startswith('http'):
                links.append(newurl)

        links = list(set(links))
        return links


def extract_content(start_url):
    #global url_dep
    telefono = []
    nombres = []
    cargo = []
    correo = []
    pagina_web = []
    redes_sociales = []
    unidad = []
    oficina = []
    google_page = []
    informacion = []
    lista = []
    news = []
    noticias = []
    fecha = []
    dia = []
    mes = []
    anio = []
    tipo = []
    titulo = []
    resumen = []
    enlace = []
    nombre_unidad = []
    # start_url= 'https://uniandes.edu.co/'

    # extrae los links donde se enumeran facultades programas y demás
    links = extract_links(start_url, 1)
    # se comienza por la url de los departamentos

    for link in links:
        print(link)
        if link.find('departamento') != -1:
            next_urls = link

            # se extraen los links que direccionan a  cada departamento
    links_departamentos = extract_links(next_urls, 2)

    # urlsdep = []

    page2 = requests.get(next_urls)
    soup2 = BeautifulSoup(page2.content, 'html.parser')

    for tag in soup2.find_all('div', class_='views-field views-field-title-1'):
        nombre_unidad.append(tag.get_text(' ', strip=True))
    # for i in range(len(links_departamentos)):
    #   if links_departamentos[i].find('c-politica') !=-1:
    #      url_dep = links_departamentos[i]
    #     nombre_departamento = nombre_unidad[i]

    for i in range(len(links_departamentos)):
        if links_departamentos[i].find('antropologia') != -1 or links_departamentos[i].find('c-politica') != -1 or \
                links_departamentos[i].find('filosofia') != -1 or links_departamentos[i].find('historia.') != -1 or \
                links_departamentos[i].find('psicologia') != -1 or links_departamentos[i].find('lenguas') != -1 or \
                links_departamentos[i].find('psicologia') != -1:
        #if links_departamentos[i].find('antropologia') != -1:
            # print(link)
            url_dep = links_departamentos[i]
            print(url_dep)
            print(" ")
            nombre_departamento = nombre_unidad[i]
            print(nombre_departamento)

        # se empieza con depto de antropologia

        #     if (link.find('c-politica') or link.find('c-politica') or link.find('filosofia') or link.find('historia') or link.find('psicologia') or link.find('lenguas') or link.find('psicologia'))!= -1:
        try:
            links_depar = extract_links(url_dep, 3)
            url_depar = links_depar[0]
            links_inner = extract_links(url_depar, 4)

            for item in links_inner:

                try:
                    if item.find('profesor') != -1:
                        url_teachers = item
                    if item.find('equipo') != -1:
                        url_employees = item
                    if item.find('noticia') != -1:
                        url_noticias = item
                except:
                    print(url_dep)
                    pass

            # url1 = 'https://antropologia.uniandes.edu.co/index.php/profesores'
            page1 = requests.get(url_teachers)
            soup1 = BeautifulSoup(page1.content, 'html.parser')
            # contenedor = soup1.find(id='scgallery')
            # profesor_items = soup1.find(class_='ot-content')
            profesor_tags = soup1.find_all(class_="cover boxcaption")

            for pt in profesor_tags:
                try:
                    nombres.append(pt.b.get_text())
                    unidad.append(nombre_departamento)
                except:
                    pass

            nombres = list(set(nombres))

            # Extraer toda la información de profesores
            for tag in soup1.find_all('div', class_='teaser-text'):
                informacion.append(tag.get_text('|', strip=True))

            # Extraer páginas web
            for tag in soup1.find_all('a', attrs={'href': re.compile('index\.php\/profesores\/\w')}):

                newurl = tag['href']
                if newurl.startswith('/'):
                    newurl = urljoin(url_teachers, newurl)
                    pagina_web.append(newurl)
            pagina_web = list(set(pagina_web))

            # for tag in soup1.find_all('div', class_='teaser-text'):
            #  informacion.append(tag.get_text())

            # eliminando duplicados
            # del(pagina_web[0:16])

            for item in informacion:
                lista.append(item.split('|'))

            # del lista[10]

            for i in range(len(lista)):
                try:
                    cargo.append(lista[i][0])
                    correo.append(lista[i][1])
                    telefono.append(lista[i][2])
                    oficina.append(lista[i][3])
                    google_page.append(" ")
                    redes_sociales.append(" ")

                except:
                    pass
            correo =list(set(correo))

            page2 = requests.get(url_employees)
            soup2 = BeautifulSoup(page2.content, 'html.parser')

            # profesor_tags = soup1.find_all(class_="cover boxcaption")

            # para extraer nombres de los empleados
            for pt in soup2.find_all(id='n1'):
                try:
                    nombres.append(pt.get_text('', strip=True))
                    unidad.append(nombre_departamento)
                except:
                    pass
            nombres = list(set(nombres))

            # Extraer información
            for tag in soup2.find_all('div', class_='teaser-text'):
                informacion.append(tag.get_text('|', strip=True))

            for item in informacion:
                lista.append(item.split('|'))

            for i in range(len(lista)):
                try:
                    cargo.append(lista[i][0])
                    correo.append(lista[i][1])
                    telefono.append(lista[i][2])
                    oficina.append(lista[i][3])
                    google_page.append(" ")
                    redes_sociales.append(" ")

                except:
                    pass
            # eventos y noticias

            page3 = requests.get(url_noticias)
            soup3 = BeautifulSoup(page3.content, 'html.parser')

            for tag in soup3.find_all('div', class_='event'):
                try:
                    news.append(tag.get_text('|', strip=True))
                except:
                    pass

            for item in news:
                try:
                    noticias.append(item.split('|'))
                except:
                    pass

            for i in range(len(noticias)):
                try:
                    dia.append(noticias[i][0])
                    mes.append(noticias[i][1])
                    anio.append(noticias[i][2])
                    tipo.append(noticias[i][3])
                    titulo.append(noticias[i][4])
                    resumen.append(noticias[i][5])
                except:
                    pass
                titulo=list(set(titulo))

            for i in range(len(dia)):
                try:
                    fecha.append(dia[i] + ' ' + mes[i] + ' ' + anio[i])
                except:
                    pass

            for tag in soup3.find_all('a', attrs={'href': re.compile('(index\.php\/noticias\/\w|index\.php\/noticias-y-eventos\/\w)')}):
                try:
                    newurl = tag['href']
                    if newurl.startswith('/'):
                        newurl = urljoin(url_noticias, newurl)
                        enlace.append(newurl)
                except:
                    pass
        except:
            pass

    return (telefono, nombres, cargo, correo,
            pagina_web, redes_sociales, unidad, oficina, google_page, fecha, tipo, titulo, resumen, enlace)


def extract_content_news(start_url):
    global url_dep

    unidad = []
    oficina = []
    google_page = []
    informacion = []
    lista = []
    news = []
    noticias = []
    fecha = []
    dia = []
    mes = []
    anio = []
    tipo = []
    titulo = []
    resumen = []
    enlace = []
    nombre_unidad = []
    # start_url= 'https://uniandes.edu.co/'

    # extrae los links donde se enumeran facultades programas y demás
    links = extract_links(start_url, 1)
    # se comienza por la url de los departamentos

    for link in links:
        print(link)
        if link.find('departamento') != -1:
            next_urls = link

            # se extraen los links que direccionan a  cada departamento
    links_departamentos = extract_links(next_urls, 2)

    # urlsdep = []

    page2 = requests.get(next_urls)
    soup2 = BeautifulSoup(page2.content, 'html.parser')

    for tag in soup2.find_all('div', class_='views-field views-field-title-1'):
        nombre_unidad.append(tag.get_text(' ', strip=True))
    # for i in range(len(links_departamentos)):
    #   if links_departamentos[i].find('c-politica') !=-1:
    #      url_dep = links_departamentos[i]
    #     nombre_departamento = nombre_unidad[i]

    for i in range(len(links_departamentos)):
        if links_departamentos[i].find('antropologia') != -1 or links_departamentos[i].find('c-politica') != -1 or \
                links_departamentos[i].find('filosofia') != -1 or links_departamentos[i].find('historia.') != -1 or \
                links_departamentos[i].find('psicologia') != -1 or links_departamentos[i].find('lenguas') != -1 or \
                links_departamentos[i].find('psicologia') != -1:
            # print(link)
            url_dep = links_departamentos[i]
            print(url_dep)
            print(" ")
            nombre_departamento = nombre_unidad[i]
            print(nombre_departamento)

        # se empieza con depto de antropologia

        #     if (link.find('c-politica') or link.find('c-politica') or link.find('filosofia') or link.find('historia') or link.find('psicologia') or link.find('lenguas') or link.find('psicologia'))!= -1:
        try:
            links_depar = extract_links(url_dep, 3)
            url_depar = links_depar[0]
            links_inner = extract_links(url_depar, 4)

            for item in links_inner:

                try:
                    if item.find('noticia') != -1:
                        url_noticias = item
                except:
                    print(url_dep)
                    pass

            # url1 = 'https://antropologia.uniandes.edu.co/index.php/profesores'

            # eventos y noticias

            page3 = requests.get(url_noticias)
            soup3 = BeautifulSoup(page3.content, 'html.parser')

            for tag in soup3.find_all('div', class_='event'):
                try:
                    news.append(tag.get_text('|', strip=True))
                except:
                    pass

            for item in news:
                try:
                    noticias.append(item.split('|'))
                except:
                    pass

            for i in range(len(noticias)):
                try:
                    dia.append(noticias[i][0])
                    mes.append(noticias[i][1])
                    anio.append(noticias[i][2])
                    tipo.append(noticias[i][3])
                    titulo.append(noticias[i][4])
                    resumen.append(noticias[i][5])
                except:
                    pass

            for i in range(len(dia)):
                try:
                    fecha.append(dia[i] + ' ' + mes[i] + ' ' + anio[i])
                except:
                    pass

            for tag in soup3.find_all('a', attrs={
                'href': re.compile('(index\.php\/noticias\/\w|index\.php\/noticias-y-eventos\/\w)')}):
                try:
                    newurl = tag['href']
                    if newurl.startswith('/'):
                        newurl = urljoin(url_noticias, newurl)
                        enlace.append(newurl)
                except:
                    pass
        except:
            pass

    return (fecha, tipo, titulo, resumen, enlace, unidad)













