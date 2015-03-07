from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('richtigTanken/index.html')