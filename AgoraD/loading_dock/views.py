from django.http import HttpResponse
from django.core import serializers
import models
from ModelGenerator import getModel
import JsonSerializer

import ModelGenerator


def index(request):
    return HttpResponse("hi")


def dblist(request, *args, **kwargs):

    t = getModel(kwargs['database'], kwargs['table'])

    #v = t(c1 = 5, c2 = "asdf")
    #v.save()

    response = HttpResponse()

    response.write(JsonSerializer.serialize(t.objects.all()))

    return response


def dbschema(request, *args, **kwargs):
    response = HttpResponse()

    response.write(models.toJSON(kwargs['database'], kwargs['table']))

    return response


def newschema(request):
    print ModelGenerator
    print ModelGenerator.data
    print ModelGenerator.data.newtable

    json = r'[{"fields": {"c2": "hello", "c1": 1}, "class": "newtable"}, {"fields": {"c2": "asdf", "c1": 5}, "class": "newtable"}]'
    
    response = HttpResponse()
    for obj in JsonSerializer.deserialize(json, 'data'):
        response.write((obj.c1, obj.c2))
  
#    json = r'[{"pk": 3, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "hello"}}, {"pk": 4, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "asdf"}}]'
    
#    for obj in serializers.deserialize('json', json):
#        print obj
    return response

