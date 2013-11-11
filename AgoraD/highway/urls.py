from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    'highway.views',
    url(r'^transfer/start/$', 'transfer_start'),
    url(r'^transfer/schema/$', 'transfer_schema'),
    url(r'^transfer/block/', 'transfer_block'),

    url(r'^intercept/schema/$', 'intercept_schema'),
    url(r'^intercept/block/$', 'intercept_block'),
)