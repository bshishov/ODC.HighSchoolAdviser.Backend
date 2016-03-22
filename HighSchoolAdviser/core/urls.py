from django.conf import settings
from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

import core
# import . as core
from core import views
from launcher import views as l
from settings import STATIC_URL, STATIC_ROOT

router = routers.DefaultRouter(trailing_slash=False)

# highschools and its results

router.register(r'highschools', views.HighSchoolsViewSet)
router.register(r'highschools/with/results', views.HighSchoolsWithResultsViewSet)
# router.register(r'highschools/with/results/by/spec', views.HighSchoolsWithResultsBySpecView)

router.register(r'results', views.OdcResultsViewSet)
# router.register(r'results/by/spec', views.OdcResultsBySpecViewSet)

# specs and groups

router.register(r'specs', views.SpecViewSet, base_name="spec")
router.register(r'specs/by/groups', views.SpecGroupViewSet)
router.register(r'groups', views.GroupViewSet)

# other

router.register(r'plans', views.PlanSet)

# patterns

urlpatterns = patterns('',
    # own
    url(r'^$', 'core.views.index'),

    # auth
    url(r'^login/$', 'core.views.login'),
    url(r'^signup/$', 'core.views.signup'),
    url(r'^signup/do/$', 'core.views.do_register'),
    url(r'^login/do/$', 'core.views.do_login'),
    url(r'^logout/do/$', 'core.views.do_logout'),

    url(r'^highschools/search/$', 'core.views.highschools_search'),
    url(r'^highschool/(?P<id>[0-9]+)/$', 'core.views.highschool'),
    url(r'^plan/(?P<plan_id>[0-9]+)/$', 'core.views.plan'),
    url(r'^spec/(?P<spec_id>[0-9]+)/$', 'core.views.spec'),
    url(r'^highschools/rating/$', 'core.views.rating'),
    url(r'^specs/$', 'core.views.specs'),

    url(r'^my/$', 'core.views.favourites'),
    url(r'^my/highschools/add/$', 'core.views.add_highschool'),
    url(r'^my/highschools/remove/$', 'core.views.add_highschool'),

    url(r'^my/plan/add/$', 'core.views.add_plan'),
    url(r'^my/plan/remove/$', 'core.views.add_plan'),

    url(r'^debug/$', 'core.views.debug'),

    # basic

    url(r'^api/', include(router.urls)),

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
