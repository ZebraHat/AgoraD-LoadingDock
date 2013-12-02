from django.conf.urls import patterns, url

from loading_dock import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^newschema/?$', views.newschema, name='newschema'),
    url(r'^insert/?$', views.newdata, name='newdata'),
    url(r'^data/(?P<database>\w+)/(?P<table>\w+)/?$', views.dbdata, name='dbdata'),
    url(r'^schema/?$', views.listdbs, name='listdbs'),
    url(r'^schema/(?P<database>\w+)/(?P<table>\w+)/?$', views.dbschema, name='dbschema'),
)

