from django.http import HttpResponse
from django.core import serializers
import models
from ModelGenerator import getModel

from ModelGenerator.data import newtable

def index(request):
    return HttpResponse("hi")

def dblist(request, *args, **kwargs):
    t = getModel(kwargs['database'], kwargs['table'])

    #v = t(c1 = 5, c2 = "asdf")
    #v.save()

    response = HttpResponse()

    serializers.serialize('json', t.objects.all(), stream=response)

    return response

def dbschema(request, *args, **kwargs):
    response = HttpResponse()

    response.write(models.toJSON(kwargs['database'], kwargs['table']))

    return response

def newschema(request):
    json = r'[{"pk": 3, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "hello"}}, {"pk": 4, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "asdf"}}]'
    
    for obj in serializers.deserialize('json', json):
        print obj

