# -*- coding: UTF-8 -*-
__author__ = 'MD'
from firstapp.util import cust_html


# 基础页设置（包含了所有页面）
class BaseViewSetting(object):
    """
    基础页设置
    """
    base_template = cust_html("base")  # 使用自定义的模板
    is_init = True  # 自定义init_app插件，初始化网站的数据
    site_icon = 'icon.png'  # site_icon插件，添加网站标题icon
    # enable_themes = True  # 内置插件，可编辑主题
    # use_bootswatch = True  # 内置插件，可改变主题