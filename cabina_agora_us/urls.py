from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from cabina_app.views import cabinarecepcion

urlpatterns = patterns('',
                       url(r'^cabinaus/', include('cabina_app.urls')),
                       url(r'^cabinarecepcion/', cabinarecepcion),

                       # url(r'^votacion/(?P<id_votacion>\w+)/$', recibe_id_votacion),

                       #  simula la url de administracion de votacion
                       # url(r'^prueba_id_votacion/(?P<id_votacion>\d+)/$', prueba_id_votacion),

                       # url(r'^prueba_id_voto/(?P<id_voto>\d+)/$', prueba_id_voto),



                       )
