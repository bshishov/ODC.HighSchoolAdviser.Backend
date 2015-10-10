from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import routers

from HighSchoolAdviser import views

router = routers.DefaultRouter()
router.register(r'highschools', views.HighSchoolsViewSet)
router.register(r'plans', views.OdcPlanSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url('^specs/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.SpecsList.as_view()),

    url(r'^$', views.index),
    url(r'^admin', include(admin.site.urls)),
)