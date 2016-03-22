from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from launcher import views
from settings import STATIC_URL, STATIC_ROOT

admin.autodiscover()

# patterns

urlpatterns = patterns('',
    url(r'^$', views.index),
) + static(STATIC_URL, document_root=STATIC_ROOT)
