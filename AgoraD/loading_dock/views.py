from django.http import HttpResponse
from django.core import serializers
from ModelGenerator import getModel, getSQL
import models
import JsonSerializer

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

    response.write(JsonSerializer.schema2json(kwargs['database'], [kwargs['table']]))

    m = getModel(kwargs['database'], kwargs['table'])

    response.write(' <br><br> ')
    for sql in getSQL(m):
        response.write(sql)

    return response

def newschema(request):
    json = '{"database": "data", "tables": {"itworks": [["a1", "(\'IntegerField\', {\'primary_key\': True})"], ["a2", "(\'TextField\', {})"]]}}'

    JsonSerializer.json2schema(json)
    response = HttpResponse()
    response.write("asf")  
    return response

def newdata(request):
    #json = r'[{"fields": {"c2": "hello", "c1": 1}, "class": "newtable"}, {"fields": {"c2": "asdf", "c1": 5}, "class": "newtable"}]'
    json = r'[{"fields": {"a2": "hello", "a1": 1}, "class": "itworks"}, {"fields": {"a2": "asdf", "a1": 5}, "class": "itworks"}]'
    
    response = HttpResponse()
    for obj in JsonSerializer.deserialize(json, 'data'):
        response.write((obj.a1, obj.a2))
        obj.save()
  
#    json = r'[{"pk": 3, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "hello"}}, {"pk": 4, "model": "loading_dock.ModelGenerator.data.newtable", "fields": {"c2": "asdf"}}]'
    
#    for obj in serializers.deserialize('json', json):
#        print obj
    return response

