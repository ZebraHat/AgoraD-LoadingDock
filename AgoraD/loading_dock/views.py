#
## views.py
## Functionality behind the loading dock urls
#

from django.http import HttpResponse
from django.core import serializers
from ModelGenerator import getModel, getSQL
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib2


import models
import JsonSerializer
import json

def index(request):
    return HttpResponse("hi")


def dbdata(request, *args, **kwargs):

    t = getModel(kwargs['database'], kwargs['table'])

    #v = t(c1 = 5, c2 = "asdf")
    #v.save()

    response = HttpResponse()

    response.write(JsonSerializer.serialize(t.objects.all()))

    return response


def dbschema(request, *args, **kwargs):
    response = HttpResponse()

    response.write(JsonSerializer.schema2json(kwargs['database'], [kwargs['table']]))

    return response

def listdbs(request):

    schema = {}

    response = HttpResponse()

    response.write(JsonSerializer.schema2json())

    return response

def newschema(request):
#    json = '{"data": {"itworks": {"a1": "(\'IntegerField\', {\'primary_key\': True})", "a2": "(\'TextField\', {})"}}}'
    json = '{"students": {"information": {"id": "(\'IntegerField\', {\'primary_key\': True})", "name": "(\'TextField\', {})", "major": "(\'TextField\', {})"}}}'

    JsonSerializer.json2schema(json)
    response = HttpResponse()
    response.write("success.")
    return response

def newdata(request):
    #json = r'[{"fields": {"c2": "hello", "c1": 1}, "class": "newtable"}, {"fields": {"c2": "asdf", "c1": 5}, "class": "newtable"}]'
    #json = r'[{"fields": {"a2": "hello", "a1": 1}, "class": "itworks"}, {"fields": {"a2": "asdf", "a1": 5}, "class": "itworks"}]'
    json = '[{"fields": {"id": 12345, "name": "jeff", "major":"CS"}, "class": "information"},{"fields": {"id": 54321, "name": "sarah", "major":"CpE"}, "class": "information"},{"fields": {"id": 666, "name": "leo", "major":"IST"}, "class": "information"}]'

    response = HttpResponse()
    for obj in JsonSerializer.deserialize(json, 'students'):
        obj.save()

#    json = r'[{"pk": 3, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "hello"}}, {"pk": 4, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "asdf"}}]'

#    for obj in serializers.deserialize('json', json):
#        print obj
    return response

def adddata(request):
    pass

@api_view(['POST'])
def addschema(request):

    for obj in JsonSerializer.deserialize(request.DATA, 'students'):
        obj.save()

    return Response(data=request.DATA, status=status.HTTP_200_OK)

