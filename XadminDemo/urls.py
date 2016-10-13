# -*- coding: UTF-8 -*-
"""XadminDemo URL Configuration

The `urlpatterns` list routes URLs to xadmin_views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function xadmin_views
    1. Add an import:  from my_app import xadmin_views
    2. Add a URL to urlpatterns:  url(r'^$', xadmin_views.home, name='home')
Class-based xadmin_views
    1. Add an import:  from other_app.xadmin_views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
import firstapp.urls
from django.views.static import serve
import settings

urlpatterns = [
    url(r"^", include(firstapp.urls)),
    # 媒体文件映射地址设置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
