from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from richtigTanken.serializers import UserSerializer, GroupSerializer, FahrtDatenSerializer, UserPositionsSerializer #hieranders
from models import FahrtDaten, UserPositions
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from models import UserPositions
import datetime



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class FahrtDatenViewSet(viewsets.ModelViewSet):
    queryset = FahrtDaten.objects.all()
    serializer_class = FahrtDatenSerializer

class UserPositionsViewSet(viewsets.ModelViewSet):
    queryset = UserPositions.objects.all()
    serializer_class = UserPositionsSerializer


def index(request):
    return render(request, 'richtigTanken/index.html')

@require_http_methods(["POST",])
def addWaypoint(request):
    json_data = json.loads(request.body)
    x = json_data['x']
    y = json_data['y']
    verbrauch = json_data['verbrauch']
    neuerWert = UserPositions.objects.create(zeit = datetime.datetime.now(), benzin_delta_in_l = verbrauch, position_x = x, position_y = y)
    neuerWert.save()
    return HttpResponse("OK")