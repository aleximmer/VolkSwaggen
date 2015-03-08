from django.conf.urls import patterns, url

from richtigTanken import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'newValue/', views.addWaypoint, name='location_update'),
    url(r'gasStations/', views.getGasStations, name='get_gasstations'),
    url(r'nearGasStations/', views.get_near_stations, name='get_near_stations'),
    url(r'allGasStations/', views.getAllGasStations, name='get_all_gasstations'),
    url(r'endRoute/', views.endRoute, name='stopRoute'),
)
