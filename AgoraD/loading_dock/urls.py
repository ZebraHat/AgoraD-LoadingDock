from django.conf.urls import patterns, url

from loading_dock import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^newschema/?$', views.newschema, name='newschema'),
    url(r'^insert/?$', views.newdata, name='newdata'),
    url(r'^(?P<database>\w+)/(?P<table>\w+)/data/?$', views.dblist, name='dblist'),
    url(r'^(?P<database>\w+)/(?P<table>\w+)/schema/?$', views.dbschema, name='dbschema'),
)

