# -*- coding: UTF-8 -*-
"""
 File Instruction
"""
__author__ = 'MD'
from django.utils.deconstruct import deconstructible
from django.contrib.auth.password_validation import *


@deconstructible
class AlwaysEqual(object):
    def __init__(self, func):
        self.func = func

    def __eq__(self, other):
        return True

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)


def validate_wrap(func):
    """
    为了让migrations不无限增加
    :param func:
    :return: AlwaysEqual
    """
    def _wrap(*args, **kwargs):
        return AlwaysEqual(func(*args, **kwargs))

    return _wrap


def _make_unicode(value):
    """
    :param value:
    :return: unicode value
    """
    try:
        ret = unicode(value)
    except:
        ret = unicode(value.decode("utf-8"))
    return ret


@validate_wrap
def validator_names_length(label_name):
    """
    名称类 字符串 长度验证器
    :param label_name:
    :return: function
    """
    return generator_value_length_validate(label_name, 1, 64)


@validate_wrap
def generator_value_length_validate(label_name, min_length=None, max_length=None):
    """
    检验值长度 验证函数生成
    :param label_name: 失败后输出的标签名称
    :param min_length: 最小长度
    :param max_length: 最大长度
    :return: function
    """

    def value_length_validator(value):
        try:
            label_length = len(_make_unicode(value))
        except:
            # 无法使用len获取value的长度
            pass

        # 最大值和最小值至少有一个有值
        if min_length is not None or max_length is not None:
            if min_length and max_length:
                if min_length > max_length:
                    if settings.DEBUG:
                        return ValidationError(message=u"最小长度不能大于最大长度！")
                else:
                    if label_length < min_length or label_length > max_length:
                        return ValidationError(message=u"{0}:长度应在{1}和{2}之间".format(label_name, min_length, max_length))
            if min_length and label_length < min_length:
                return ValidationError(message=u"{0}：长度不应小于{1}".format(label_name, min_length))
            if max_length and label_length > max_length:
                return ValidationError(message=u"{0}：长度不应大于{1}".format(label_name, max_length))
        # 最大值和最小值都为空
        else:
            pass

    return value_length_validator
