from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import routers

from HighSchoolAdviser import views

router = routers.DefaultRouter()
router.register(r'highschools', views.HighSchoolsViewSet)
router.register(r'plans', views.PlanSet)
router.register(r'specs', views.SpecViewSet)
router.register(r'spec_groups', views.SpecGroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),

    url('^plans_by_spec/(?P<spec_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansBySpecList.as_view()),
    url('^plans_by_group/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansByGroupList.as_view()),

    url('^specs_by_group/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.SpecsByGroupList.as_view()),
    url('^search/(?P<spec_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.SearchList.as_view()),

    url(r'^$', views.index),
    url(r'^admin', include(admin.site.urls)),
)