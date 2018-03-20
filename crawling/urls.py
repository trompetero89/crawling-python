from django.conf.urls import url
from django.views.generic import TemplateView


from . import views

app_name = 'crawling'
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^noticias/$', views.noticias, name='noticias'),
    url(r'^dependencias/$',views.dependencias, name='dependencias'),
    url(r'^rssfeed/$',views.rssfeed, name='rssfeed'),
    url(r'^home/$', views.home, name='home'),

]