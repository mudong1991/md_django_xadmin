# -*- coding: UTF-8 -*-
__author__ = 'MD'
from rest_framework import pagination
from rest_framework.views import Response


# 自定义分页类
class CustomPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "rows"  # 分页的项集合

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'total': self.page.paginator.num_pages,
            'records': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'rows': data,
        })
