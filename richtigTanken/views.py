from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from richtigTanken.serializers import UserSerializer, GroupSerializer, FahrtDatenSerializer, UserPositionsSerializer #hieranders
from models import FahrtDaten, UserPositions
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from models import UserPositions, FahrtDaten, Tankstellen
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

@require_http_methods(["POST"])
def addWaypoint(request):
    json_data = json.loads(request.body)
    x = json_data['x']
    y = json_data['y']
    verbrauch = json_data['verbrauch']
    neuerWert = UserPositions.objects.create(zeit = datetime.datetime.now(), benzin_delta_in_l = verbrauch, position_x = x, position_y = y)
    neuerWert.save()
    return HttpResponse("OK")

def getAllGasStations(request):
    data = { 'stations': [] }

    for elem in Tankstellen.objects.all():
        station = {
            'name': elem.bezeichnung,
            'lat': elem.position_x,
            'lng': elem.position_y
        }
        data['stations'].append(station)

    return JsonResponse(data, safe=False)


def getGasStations(request):
    #json_text = '{"stations":['
    #for elem in Tankstellen.objects.all():
    #    json_text = json_text + '{' + "name:" + elem.bezeichnung + ',' + "lat:" + str(elem.position_x) + ',' + "lng:" + str(elem.position_y) + '},'

    #json_text = json_text + ']}'
    #print(json_text)
    #json.loads(json_text)
    data = {
        'stations': [
            { 'lat': 52.53398, 'lng': 13.409852 },
            { 'lat': 52.50178, 'lng': 13.404832 },
            { 'lat': 52.50048, 'lng': 13.409842 },
            { 'lat': 52.50195, 'lng': 13.406882 },
        ]
    }
    response = JsonResponse(data, safe=False)
    return response

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


def normalize(vector, user_position):
    #500m distance to next station
    distance = 0.5 
    length_km = distance_on_unit_sphere(user_position.position_x, user_position.position_y, (user_position.position_x+vector[0]), (user_position.position_y+vector[1]))
    norm = 0.5/length_km
    vector[0] = vector[0] * norm
    vector[1] = vector[1] * norm
    return vector

def get_near_stations():
    waypoints = UserPositions.objects.all().order_by['zeit']
    direction = [0.0,0.0]
    cur = waypoints[0]
    for elem in waypoints:
        direction[0] = direction[0] + (elem.position_x - cur.position_x)
        direction[1] = direction[1] + (elem.position_y - cur.position_y)
        cur = elem
    direction = normalize(direction, waypoints[0])
    direction_rotate = [(direction[1]/2), (-direction[0]/2)]
    





