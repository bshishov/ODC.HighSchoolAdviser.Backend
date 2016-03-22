from django.conf.urls import include, url

urlpatterns = [
    url(r'^core/', include('core.urls')),
    url(r'^launcher/', include('launcher.urls')),
]