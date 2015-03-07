from django.conf.urls import patterns, url

from richtigTanken import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<x_value>\d+)/(?P<y_value>\d+)/$', views.addWaypoint, name='location_update')
)