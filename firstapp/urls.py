# -*- coding: UTF-8 -*-
__author__ = 'MD'
from django.conf.urls import include, url
from xadmin_views import *

# 自动初始化xadmin
import xadmin
xadmin.autodiscover()

# 自动初始化firstapp
import firstapp
firstapp.autodiscover()


urlpatterns = [
    url(r"^", include(xadmin.site.urls)),

    url(r'^session/', SessionTimeOut.as_view()),

    # vdp-api
    url(r'^api/', include("firstapp.apiurls")),
]
