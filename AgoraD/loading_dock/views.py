from django.http import HttpResponse
from django.core import serializers
from ModelGenerator import getModel

def index(request):
    return HttpResponse("hi")

def dblist(request, *args, **kwargs):
    t = getModel(kwargs['database'], kwargs['table'])

    #v = t(c1 = 5, c2 = "asdf")
    #v.save()

    response = HttpResponse()

    serializers.serialize('json', t.objects.all(), stream=response)

    return response


