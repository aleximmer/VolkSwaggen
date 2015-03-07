from django.conf.urls import url, include, patterns
from rest_framework import routers
from richtigTanken import views
from django.contrib import admin


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'fahrtdaten', views.FahrtDatenViewSet)
router.register(r'userpositions', views.UserPositionsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^richtigTanken/', include('richtigTanken.urls')),
]
