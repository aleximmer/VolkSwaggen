from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from richtigTanken.serializers import UserSerializer, GroupSerializer, FahrtDatenSerializer, UserPositionsSerializer #hieranders
from models import FahrtDaten, UserPositions


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