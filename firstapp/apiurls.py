# -*- coding: UTF-8 -*-
__author__ = 'MD'
from django.conf.urls import url, patterns
from firstapp import apiviews
from rest_framework import routers


urlpatterns = [
    url(r"^systeminfo", apiviews.systeminfo),
    url(r'^sync_time/', apiviews.GetSystemTime.as_view()),
]

route = routers.DefaultRouter()
route.register(r"^bookborrowinfo", apiviews.BookBorrowInfoSet)

urlpatterns += route.urls

