from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from core import views
from settings import STATIC_URL, STATIC_ROOT

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

admin.autodiscover()


# patterns

urlpatterns = patterns('',
    # own
    url(r'^$', views.index),

    # auth
    url(r'^login/$', views.login),
    url(r'^signup/$', views.signup),
    url(r'^signup/do/$', views.do_register),
    url(r'^login/do/$', views.do_login),
    url(r'^logout/do/$', views.do_logout),

    url(r'^highschools/search/$', views.highschools_search),
    url(r'^highschool/(?P<id>[0-9]+)/$', views.highschool),
    url(r'^plan/(?P<plan_id>[0-9]+)/$', views.plan),
    url(r'^spec/(?P<spec_id>[0-9]+)/$', views.spec),
    url(r'^highschools/rating/$', views.rating),
    url(r'^specs/$', views.specs),

    url(r'^my/$', views.favourites),
    url(r'^my/highschools/add/$', views.add_highschool),
    url(r'^my/highschools/remove/$', views.add_highschool),

    url(r'^my/plan/add/$', views.add_plan),
    url(r'^my/plan/remove/$', views.add_plan),

    url(r'^debug/$', views.debug),

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
) + static(STATIC_URL, document_root=STATIC_ROOT)
