# -*- coding: UTF-8 -*-
__author__ = 'MD'
from rest_framework import serializers
from firstapp import models


class BookBorrowInfoSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name')
    student_name = serializers.CharField(source="student.name")

    class Meta:
        model = models.BookBorrowInfo
        fields = "__all__"
