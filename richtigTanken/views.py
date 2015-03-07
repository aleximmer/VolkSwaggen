from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from richtigTanken.serializers import UserSerializer, GroupSerializer, FahrtDatenSerializer, UserPositionsSerializer #hieranders
from models import FahrtDaten, UserPositions
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from models import UserPositions, FahrtDaten
import datetime
import math



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


def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # return in kilometres
    return (arc * 6371)

@require_http_methods(["POST",])
def endRoute(request):
    positionen = UserPositions.objects.all().order_by('zeit')
    current_pos = positionen[0]
    distance = 0
    verbrauch = 0
    for elem in positionen:
        delta = distance_on_unit_sphere(float(current_pos.position_x), float(current_pos.position_y), float(elem.position_x), float(elem.position_y))
        distance = distance + delta
        current_pos = elem
        verbrauch = verbrauch + elem.benzin_delta_in_l
        last_zeit = elem.zeit
    distance = float('%.1f' % distance)
    verbrauch = float('%.2f' % verbrauch)
    print(distance)
    print(verbrauch)
    print(request.user)
    FahrtDaten.objects.create(nutzer = request.user, strecken_laengekm = distance, spritverbrauch_in_l = verbrauch, start_zeit = positionen[0].zeit, end_zeit = last_zeit).save()
    return HttpResponse("OK")



