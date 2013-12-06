#
## urls.py
## URLs specific to the loading_dock
#

from django.conf.urls import patterns, url

from loading_dock import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^newschema/?$', views.newschema, name='newschema'),
    url(r'^newdata/?$', views.newdata, name='newdata'),
    url(r'^add-schema/?$', views.addschema, name='addschema'),
    url(r'^add-data/?$', views.adddata, name='adddata'),
    url(r'^data/(?P<database>\w+)/(?P<table>\w+)/?$', views.dbdata, name='dbdata'),
    url(r'^schema/?$', views.listdbs, name='listdbs'),
    url(r'^schema/(?P<database>\w+)/(?P<table>\w+)/?$', views.dbschema, name='dbschema'),
)

