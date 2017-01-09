from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from cabina_app.views import cabinarecepcion ,recibe_id_votacion, recibe_id_votacion_fromdb



urlpatterns = patterns('',
                       #url(r'^/$', include('cabina_app.urls')),
                       #url(r'^(?P<id_poll>\d+)/$',recibe_id_votacion),
                       #Simula la renderizacion de un index a partir de un id de Question
                       url(r'^votacion/(?P<id_poll>\w+)/$', recibe_id_votacion),
                       url(r'^cabinarecepcion/$', cabinarecepcion),
                       url(r'', include('cabina_app.urls')),




                       #  simula la url de administracion de votacion
                       # url(r'^prueba_id_votacion/(?P<id_votacion>\d+)/$', prueba_id_votacion),

                       # url(r'^prueba_id_voto/(?P<id_voto>\d+)/$', prueba_id_voto),



                       )
