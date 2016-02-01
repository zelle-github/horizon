from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls', namespace='home')),
    #url(r'^login/', 'django.contrib.auth.views.login'),
    #url(r'^logout/', 'django.contrib.auth.views.logout'),
    url(r'^databrowser/', include('databrowser.urls', namespace='databrowser')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
