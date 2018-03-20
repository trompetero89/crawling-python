from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.views import generic
from django.views import View
# Create your views here.
from bs4 import BeautifulSoup
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from . import crawling_personas

#from fake_useragent import UserAgent
#import scrapy
#import django_tables2 as tables






def index(request):
        template = loader.get_template('crawling/index.html')
        context = {'animal': 'perro'}
        return render(request, 'crawling/index.html', context)

def home(request):
    # <script type="text/javascript" language="javascript" src="TableFilter/tablefilter.js"></script>

    response = 'lala'


    return render(request, 'crawling/home.html')



def rssfeed(request):
    response = 'para msotrar el rss'



    fuentes = ['http://www.espn.com/espn/rss/nba/news',
               'http://www.espn.com/espn/rss/nfl/news',
               'http://www.espn.com/espn/rss/rpm/news',
               'https://api.foxsports.com/v1/rss?partnerKey=zBaFxRyGKCfxBagJG9b8pqLyndmvo7UU&tag=nfl',
               'https://api.foxsports.com/v1/rss?partnerKey=zBaFxRyGKCfxBagJG9b8pqLyndmvo7UU&tag=motor',
               'https://api.foxsports.com/v1/rss?partnerKey=zBaFxRyGKCfxBagJG9b8pqLyndmvo7UU&tag=nba',
               'https://www.si.com/rss/si_nfl.rss', 'https://www.si.com/rss/si_nba.rss']

    return render(request, 'crawling/rssfeed.html')



def noticias(request):
    url_raiz = 'https://uniandes.edu.co/'
    telefono, nombres, cargo, correo, pagina_web, redes_sociales, unidad, oficina, google_page, fecha, tipo, titulo, resumen, enlace = crawling_personas.extract_content(
        url_raiz)
    #fecha = [u'meal', u'personal', u'sleep', u'transport', u'work']
    #tipo =
    #titulo = ['0:08:35.882945', 0, 0, 0, 0]
    #resumen = ['0:08:35.882945', 0, 0, 0, 0]
    #enlace = ['0:08:35.882945', 0, 0, 0, 0]
    #unidad = ['0:08:35.882945', 0, 0, 0, 0]



    noticias = zip(fecha, titulo, resumen, enlace, unidad)
    num = 56
    context = {
       'MyList': noticias, 'numer': num
    }

    response = 'Este es para mostrar las noticias'

    return render(request, 'crawling/noticias.html', context)

def dependencias(request):
    response = 'Aquí se muestran las dependencias'


    url_raiz = 'https://uniandes.edu.co/'
    telefono, nombres, cargo, correo, pagina_web, redes_sociales, unidad, oficina, google_page, fecha, tipo, titulo, resumen, enlace = crawling_personas.extract_content(
        url_raiz)


    #url = 'uniandes'
    #nombres, cargo, correo, oficina, telefono, pagina_web, google_page, redes_sociales, unidad = crawling_personas.extractCivil(url)

    #return nombre, cargo, correo, oficina, telefono, pagina_web, google, redes_sociales, unidad


    nob = zip(nombres, cargo, correo,oficina,telefono,pagina_web,google_page,redes_sociales,unidad)
    num=56
    context ={
    'MyList':nob, 'numer':num
    }


    return render(request,'crawling/dependencias.html', context )

#class DependenciasView(View):
 #   def get(self, request, *args, **kwargs):
  #      context = {}
   #     return render(request, 'crawling/dependencias.html', context)

#class DependenciasTemplateView(TemplateView):
 #   template_name ='crawling/dependencias.html'
