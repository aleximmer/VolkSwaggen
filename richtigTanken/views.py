from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from richtigTanken.serializers import UserSerializer, GroupSerializer, FahrtDatenSerializer, UserPositionsSerializer #hieranders
from models import FahrtDaten, UserPositions
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



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

class SnippetList(APIView):

    def get(self, request, formart=None):
    snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)