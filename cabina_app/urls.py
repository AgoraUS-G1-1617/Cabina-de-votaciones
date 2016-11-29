from django.conf.urls import patterns, url
from cabina_app import views

urlpatterns = patterns('',
                       url(r'^(?P<id_poll>\d+)/$', views.recibe_id_votacion,name='home'),
                       url(r'', views.recibe_id_votacion)
                       )
