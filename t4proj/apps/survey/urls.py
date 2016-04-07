# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^survey/$', views.index, name='index'),
    url(r'room/(?P<room_slug>[-\w]+)/survey$', views.survey, name='survey'),
    url(r'room/(?P<room_slug>[-\w]+)/thanks$', views.thanks, name='thanks'),
]