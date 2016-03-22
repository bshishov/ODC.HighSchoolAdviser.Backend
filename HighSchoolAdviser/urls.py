from django.conf.urls import include, url
from django.contrib import admin
from core import urls as core_urls
from launcher import urls as launcher_urls

admin.autodiscover()

urlpatterns = [
    url(r'^$', include(launcher_urls)),   
    url(r'^alpha/', include(core_urls)),
    url(r'^admin/', include(admin.site.urls)),
]