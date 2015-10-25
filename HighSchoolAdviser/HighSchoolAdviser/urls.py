from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from HighSchoolAdviser import views

router = routers.DefaultRouter(trailing_slash=False)

# highschools and its results

router.register(r'highschools', views.HighSchoolsViewSet)
router.register(r'highschools/with/results', views.HighSchoolsWithResultsViewSet)
# router.register(r'highschools/with/results/by/spec', views.HighSchoolsWithResultsBySpecView)

router.register(r'results', views.OdcResultsViewSet)
# router.register(r'results/by/spec', views.OdcResultsBySpecViewSet)


# specs and groups

router.register(r'specs', views.SpecViewSet)
router.register(r'specs/by/groups', views.SpecGroupViewSet)
router.register(r'groups', views.GroupViewSet)

# other

router.register(r'plans', views.PlanSet)


# patterns

urlpatterns = patterns('',

    # basic

    url(r'^api/', include(router.urls)),
    url(r'^api/admin/', include(admin.site.urls)),

    # filters

    url(r'^api/highschools/(?P<highschool_id>[0-9]+)/spec/(?P<spec_id>[0-9]+)/results\.(?P<format>[a-z0-9]+)/$', views.HighSchoolsWithResultsBySpecView.as_view()),

    # url(r'^api/highschools/group_results/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.HighSchoolsWithResultsByGroupViewSet.as_view()),

    # url(r'^api/plans_by_spec/(?P<spec_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansBySpecList.as_view()),
    # url(r'^api/plans_by_group/(?P<group_id>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.PlansByGroupList.as_view()),

    url(r'^api/search\.(?P<format>[a-z0-9]+)/$', views.SearchList.as_view()),
    # url(r'^api/search/totals\.(?P<format>[a-z0-9]+)/$', views.SearchTotalsList.as_view()),

    url(r'api/result/bins\.(?P<format>[a-z0-9]+)/$', views.Search1.as_view()),
    url(r'api/result/bins/(?P<highschool>[0-9]+)\.(?P<format>[a-z0-9]+)/$', views.Search2.as_view()),
)