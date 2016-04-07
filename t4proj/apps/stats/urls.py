# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^explore$', views.explore, name='explore'),
    url(r'^log$', views.log, name='log'),
]