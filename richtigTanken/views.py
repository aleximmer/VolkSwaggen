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
from models import UserPositions, FahrtDaten, Tankstellen, BenzinPreis
import datetime
import math
import copy



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

class BenzinPreisViewSet(viewsets.ModelViewSet):
    queryset = BenzinPreis.objects.all()

def index(request):
    return render(request, 'richtigTanken/index.html')

@require_http_methods(["POST"])
def addWaypoint(request):
    json_data = json.loads(request.body)
    x = json_data['lat']
    y = json_data['lng']
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

distance = float(0.4)
def normalize(vector, user_position):
    #500m distance to next station
    length_km = distance_on_unit_sphere(float(user_position.position_x), float(user_position.position_y), (float(user_position.position_x)+vector[0]), (float(user_position.position_y)+vector[1]))
    norm = distance/length_km
    vector[0] = vector[0] * norm
    vector[1] = vector[1] * norm
    return vector


def get_around_stations():
    cur = UserPositions.objects.all().order_by('-zeit')[0]
    stations = list(Tankstellen.objects.all())
    stationsSammel = copy.deepcopy(stations)
    for elem in stationsSammel:
        dist = float(distance_on_unit_sphere(float(cur.position_x), float(cur.position_y), float(elem.position_x), float(elem.position_y)))
        print(dist)
        if dist > distance:
            stations.remove(elem)
            print(elem.bezeichnung)
    return stations


def get_near_stations(request):
    waypoints = UserPositions.objects.all().order_by('zeit')
    direction = [0.0,0.0]
    cur = waypoints[0]
    for elem in waypoints:
        direction[0] = direction[0] + float(elem.position_x - cur.position_x)
        direction[1] = direction[1] + float(elem.position_y - cur.position_y)
        cur = elem
    direction = normalize(direction, waypoints[0])
    direction_rotate = [direction[1], -direction[0]]
    left_point  = [float(cur.position_x) - 0.5 * direction_rotate[0], float(cur.position_y) - 0.5 * direction_rotate[1]]
    stations = get_around_stations()
    stationsSammel = copy.deepcopy(stations)
    for station in stationsSammel:
        helper = (float(station.position_x) - left_point[0]) / direction_rotate[0]
        if (direction_rotate[1] * helper + left_point[1] < station.position_y):
            stations.remove(station)
    data = { 'stations': [] }

    for elem in stations:
        station = {
            'name': elem.bezeichnung,
            'lat': elem.position_x,
            'lng': elem.position_y
        }
        data['stations'].append(station)

    return JsonResponse(data, safe=False)


def get_reach(fuel_level):
    average_consumption = get_average_consumption_per_day()
    lasting_days = 0
    today = datetime.datetime.now().date()
    day = today - datetime.timedelta(days=7)

    def get_daily_absolute_consumption(dayy):
        drives = list(FahrtDaten.objects.all())
        consumption = 0

        for drive in copy.deepcopy(drives):
            if drives.start_zeit.date() != dayy:
                drives.remove(drive)

        for drive in drives:
            consumption = consumption + drive.spritverbrauch_in_l

        return consumption

    while fuel_level > 0 and day != today:
        lasting_days = lasting_days + 1
        fuel_level = fuel_level - average(get_average_daily_consumption(day), average_consumption)
        day = day + datetime.timedelta(days=1)

    return lasting_days


def average(val1, val2):
    return (val1 + val2) / 2


def get_trends(daysCount):
    today = datetime.datetime.now().date()
    result = []

    year = 2015
    month = 02
    day = 8
    hour = 16

    for i in range(0,daysCount):
        date = datetime.datetime(year, month, day + i, hour)
        tanken = BenzinPreis.objects.all().filter(start_zeit=date)

        tankenPreis = 0
        for tanke in tanken:
            tankenPreis = tankenPreis + tanke.preis

        result.append(gesamtPreis / len(tanken))
    return result


def get_average_consumption_per_track():
    drives = FahrtDaten.objects.all()
    consumption = 0
    track = 0

    for drive in drives:
        consumption = consumption + drive.spritverbrauch_in_l
        track = track + drive.streckenlaengekm

    return consumption / track


def get_average_consumption_per_day():
    drives = FahrtDaten.objects.all()
    consumption = 0

    for drive in drives:
        consumption = consumption + drive.spritverbrauch_in_l

    return consumption / 14
