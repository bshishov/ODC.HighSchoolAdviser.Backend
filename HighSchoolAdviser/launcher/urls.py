from django.conf.urls import patterns, include, url

from launcher import views

urlpatterns = patterns('',
    url(r'^$', views.index),
)
