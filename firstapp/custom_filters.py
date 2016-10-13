# -*- coding: UTF-8 -*-
__author__ = 'MD'
import django_filters
from firstapp import models
from rest_framework import filters


class BookBorrowInfoFilter(filters.FilterSet):
    book_id = django_filters.NumberFilter(name='book__pk')

    class Meta:
        model = models.BookBorrowInfo
