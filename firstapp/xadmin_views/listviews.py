# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views import ListAdminView
from xadmin.plugins import actions
from django.utils.translation import ugettext_lazy as _, ungettext
from firstapp.util import cust_html



class CustomDeleteSelectedAction(actions.DeleteSelectedAction):
    description = _('Delete selected %(verbose_name_plural)s')  # 重写描述信息，修改语言显示bug


# 列表页设置（列出数据的页面）
class ListPageViewSetting(ListAdminView):
    # 定时刷新定义
    refresh_times = (3, 5, 10)
    # 分页大小
    list_per_page = 10

    # 全局数据操作
    global_actions = [CustomDeleteSelectedAction]

    # 布局风格
    # grid_layouts = ['table', 'thumbnails']  # 这个插件与自定义模板冲突
    object_list_template = cust_html('cust_model_list')