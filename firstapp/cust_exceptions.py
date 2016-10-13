# -*- coding: utf-8 -*-
__author__ = 'MD'

from rest_framework.exceptions import APIException


class SocketUnavailable(APIException):
    status_code = 503
    default_detail = '套接字通信错误'


class VdpOperationFailed(APIException):
    status_code = 503
    default_detail = '操作失败'


class ValidationFailed(APIException):
    status_code = 400
    default_detail = '数据未通过内部验证！请检查数据是否被破坏!'


class NeedRedirectOperatingException(APIException):
    status_code = 304
    is_set_client_message = False
    error_msg_key = ''
    default_detail = "需要重定向"
    redirect_url = '/'

    def __init__(self, redirect_url="/", is_set_client_message=False, error_msg_key='', default_detail=''):
        self.redirect_url = redirect_url
        self.is_set_client_message = is_set_client_message
        self.default_detail = default_detail
        self.error_msg_key = error_msg_key
