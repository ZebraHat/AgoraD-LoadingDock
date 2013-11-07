from django.http import HttpResponse
import ModelGenerator
from ModelGenerator import data
from ModelGenerator.data import newtable

def index(request):
  return HttpResponse("hi")

def dblist(request, *args, **kwargs):
  print ModelGenerator
  t = ModelGenerator.getModel(kwargs['database'], kwargs['table'])

  print ModelGenerator.data

  print t
  s = ''
  for i in t.objects.all():
    s += str((i.c1, i.c2))

  return HttpResponse(s)


