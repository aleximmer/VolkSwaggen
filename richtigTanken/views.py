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

tankstand = 45.0

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

#tankstand = 50

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
    UserPositions.objects.all().delete()
    global tankstand
    tankstand = 45.0
    print(distance)
    print(verbrauch)
    print(request.user)
    #FahrtDaten.objects.create(nutzer = request.user, strecken_laengekm = distance, spritverbrauch_in_l = verbrauch, start_zeit = positionen[0].zeit, end_zeit = last_zeit).save()
    return HttpResponse("OK")

distance = float(0.5)
def normalize(vector, user_position):
    length_km = distance_on_unit_sphere(float(user_position.position_x), float(user_position.position_y), (float(user_position.position_x)+vector[0]), (float(user_position.position_y)+vector[1]))
    norm = distance/length_km
    vector[0] = vector[0] * norm
    vector[1] = vector[1] * norm
    return vector


def get_around_stations():
    cur = UserPositions.objects.all().order_by('-zeit')[0]
    stations = list(Tankstellen.objects.all().order_by('preis'))
    stationsSammel = copy.deepcopy(stations)
    for elem in stationsSammel:
        dist = float(distance_on_unit_sphere(float(cur.position_x), float(cur.position_y), float(elem.position_x), float(elem.position_y)))
        if dist > distance:
            stations.remove(elem)
    return stations

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

def get_ersparnis(tankstand, stations):
    tankenPreis = get_trends(get_reach(tankstand))
    # teste trend fuer tankenPreis[0] und vergleiche mit umgebenden tankstellen (aktuelle preise)
    stations = sorted(stations, key=lambda station: station.preis)
    stations = stations[0:3]
    if not stations:
        return [], 0
    # 60 liter tank
    tankstand = tankstand / 60.0
    tankval = 1.0 - float(tankstand/2.0)
    tankstand = tankstand * 60.0
    #print(float(stations[0].preis))
    #print(tankenPreis[0])
    #if (float(stations[0].preis) * float(tankval)) > tankenPreis[0]:
#        print("hier null")
#        return [], 0

    for elem in copy.deepcopy(stations):
        if (float(elem.preis) * tankval) > tankenPreis[0]:
            stations.remove(elem)

    if not stations:
        return [], 0

    max_ersparnis = (float(tankenPreis[0]) - float(stations[0].preis)) * (60.0-float(tankstand))
    print("Maximale ersparnis: %s" % max_ersparnis)
    return stations, max_ersparnis

def average(val1, val2):
    return (val1 + val2) / 2

def get_average_consumption_per_day():
    drives = FahrtDaten.objects.all()
    consumption = 0

    for drive in drives:
        consumption = consumption + drive.spritverbrauch_in_l

    return consumption / 14

def get_reach(fuel_level):
    average_consumption = get_average_consumption_per_day()
    lasting_days = 0
    today = datetime.datetime.now().date()
    day = today - datetime.timedelta(days=7)

    def get_daily_absolute_consumption(dayy):
        drives = list(FahrtDaten.objects.all())
        consumption = 0

        for drive in copy.deepcopy(drives):
            if drive.start_zeit.date() != dayy:
                drives.remove(drive)

        for drive in drives:
            consumption = consumption + drive.spritverbrauch_in_l

        return float(consumption)

    while fuel_level > 0 and day != today:
        lasting_days = lasting_days + 1
        fuel_level = fuel_level - average(get_daily_absolute_consumption(day), float(average_consumption))
        day = day + datetime.timedelta(days=1)

    return lasting_days


def get_trends(daysCount):
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
        if tanken:
            result.append(tankenPreis / len(tanken))
    return result


def get_average_consumption_per_track():
    drives = FahrtDaten.objects.all()
    consumption = 0
    track = 0

    for drive in drives:
        consumption = consumption + drive.spritverbrauch_in_l
        track = track + drive.streckenlaengekm

    return consumption / track

def get_near_stations(request, tankstand):
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

    for station in stations:
        print(station.bezeichnung)

    stations, max_ersparnis = get_ersparnis(tankstand, stations)

    if max_ersparnis > 0:
        max_ersparnis = max_ersparnis + 0.5
    if max_ersparnis < 0:
        max_ersparnis = 0

    farbe = 'green'
    if tankstand < 40.0:
        farbe = 'gelb'
    if tankstand < 20.0:
        farbe = 'rot'

    data = {
            'ersparnis': max_ersparnis,
            'farbe': farbe,
            'stations': [] }

    for elem in stations:
        station = {
            'name': elem.bezeichnung + " %s" % float(elem.preis),
            'lat': elem.position_x,
            'lng': elem.position_y
        }
        data['stations'].append(station)

    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
def addWaypoint(request):
    json_data = json.loads(request.body)
    x = json_data['lat']
    y = json_data['lng']
    verbrauch = json_data['verbrauch']
    neuerWert = UserPositions.objects.create(zeit = datetime.datetime.now(), benzin_delta_in_l = verbrauch, position_x = x, position_y = y)
    neuerWert.save()
    global tankstand
    tankstand = float(tankstand) - 0.7
    if tankstand < 5:
        tankstand = 20
    return get_near_stations(request, tankstand)
