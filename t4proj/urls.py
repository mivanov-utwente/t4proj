"""t4proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from . import settings


urlpatterns = [
    url(r'^$', 't4proj.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/', include('t4proj.apps.stats.urls', 'stats')),
    url(r'', include('t4proj.apps.survey.urls', 'survey')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
