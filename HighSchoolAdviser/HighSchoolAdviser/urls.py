from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from HighSchoolAdviser import views

router = routers.DefaultRouter(trailing_slash=False)


# highschools and its results

router.register(r'highschools', views.HighSchoolsViewSet)
router.register(r'results', views.OdcResultsViewSet)
# router.register(r'results/by/spec', views.OdcResultsBySpecViewSet)
router.register(r'highschools/with/results', views.HighSchoolsWithResultsViewSet)
# router.register(r'highschools/with/results/by/spec', views.HighSchoolsWithResultsBySpecView)


# specs and groups

router.register(r'specs', views.SpecViewSet)
router.register(r'specs/by/groups', views.SpecGroupViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'plans', views.PlanSet)


# patterns

urlpatterns = patterns('',
    url(r'^', include(router.urls)),

    url('^highschools/(?P<highschool_id>[0-9]+)/spec/(?P<spec_id>[0-9]+)/results\.(?P<format>[a-z0-9]+)/$', views.HighSchoolsWithResultsBySpecView.as_view()),

    # url('^highschools/group_results/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.HighSchoolsWithResultsByGroupViewSet.as_view()),

    url('^plans_by_spec/(?P<spec_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansBySpecList.as_view()),
    url('^plans_by_group/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansByGroupList.as_view()),

    url('^search/(?P<spec_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.SearchList.as_view()),

    url(r'^$', views.index),
    url(r'^admin', include(admin.site.urls)),
)