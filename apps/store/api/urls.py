# -*- coding: utf-8 -*-
from django.urls import path
from .views import stations


urlpatterns = [
    path('stations/', stations.as_view(), name='stations_api'),
]
