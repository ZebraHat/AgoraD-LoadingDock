from django.conf.urls import patterns, url

from loading_dock import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<database>\w+)/(?P<table>\w+)/?$', views.dblist, name='dblist'),
)

