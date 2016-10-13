# -*- coding: UTF-8 -*-
__author__ = 'MD'
from django.shortcuts import render


class CustomAuthorizeMiddleWare(object):
    """
    权限定义中间件
    """
    def process_response(self, request, response):
        """
        HttpResponse重写
        :param request:
        :param response:
        :return:
        """
        # 页面没有权限的情况处理
        if response.status_code == 403:
            return render(request, 'error_info.html', {"message": "您没有权限访问这个页面！", "status_code": 403}, status=403)
        if response.status_code == 404:
            return render(request, 'error_info.html', {"message": "找不到指定页面！", "status_code": 404}, status=404)
        return response
