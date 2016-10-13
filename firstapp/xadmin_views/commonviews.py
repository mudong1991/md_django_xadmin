# -*- coding: UTF-8 -*-
__author__ = 'MD'
"""
通用视图相关
"""
from firstapp.util import cust_html
from xadmin.views import CommAdminView
from firstapp.models import *
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from xadmin.views.base import filter_hook
from rest_framework.views import APIView, Response
from django.contrib.auth import logout
from firstapp import util
from xadmin.plugins.auth import ChangeAccountPasswordView, ChangePasswordView
from firstapp.forms import CustomPasswordChangeForm, CustomAdminPasswordChangeForm


# 全局设置（用户登录认证后的的公共页）
class CommonViewSetting(CommAdminView):
    """
    全局设置
    """
    base_template = cust_html("base_site")   # 使用自定义的模板
    cust_menu_style = 'cust_accordion'  # 自定义的插件的菜单风格
    show_time = True

    def get_site_menu(self):
        """
        自定义菜单
        :return:
        """
        super(CommonViewSetting, self).get_site_menu()
        return (
            # 主页
            {'title': _('Index'), 'icon': 'fa-fw fa fa-home', 'menus':(
                {'title': _('home'), 'icon': 'fa-fw fa fa-home', 'url': '/index/'},
                {'title': _('system status'), 'icon': 'fa fa-television', 'url': '/running/'},
            )},

            # 图书管理
            {'title': _('Book management'),  'icon': 'fa fa-building',
             'menus': (
                 {'title': _('book'), 'icon': 'fa fa-book', 'url': self.get_model_url(Book, 'changelist'),
                  'perm': self.get_model_perm(Book, 'change')},
             )},

            # 日志管理
            {'title': _('Log management'),  'icon': 'fa-fw fa fa-edit',
             'menus': (
                {'title': _('user log'), 'icon': 'fa-fw fa fa-eye', 'url': self.get_model_url(UserLogs, 'changelist')},
                {'title': _('warning log'), 'icon': 'fa-fw fa fa-bell', 'url': self.get_model_url(WarningLogs, 'changelist'),
                 'perm': self.get_model_perm(WarningLogs, 'change')},
            )},

            # 用户管理
            {'title': _('User management'),  'icon': 'fa-fw fa fa-lock', 'menus': (
                {'title': _('group'), 'icon': 'fa-fw fa fa-group', 'url': self.get_model_url(Group, 'changelist'),
                 'perm': self.get_model_perm(Group, 'change')},
                {'title': _('user'), 'icon': 'fa-fw fa fa-user', 'url': self.get_model_url(User, 'changelist'),
                 'perm': self.get_model_perm(User, 'change')},
                {'title': _('permission'), 'icon': 'fa-fw fa fa-lock', 'url':
                    self.get_model_url(Permission, 'changelist'), 'perm': self.get_model_perm(Permission, 'change')},
            )},
        )

    def get_nav_menu(self):
        """
        生成菜单，清除原有的菜单项
        :return:
        """
        return self.get_site_menu()

    @filter_hook
    def get_breadcrumb(self):
        """
        重写首页的地址，指定到自定义的首页地址
        :return:
        """
        return [{
            'url': self.get_admin_url('custom_index'),
            'title': _('Home')
        }]


# 验证session
class SessionTimeOut(APIView):
    def get(self, request):
        result = {'msg': '', 'resultcode': 0}
        # 匿名用户
        if request.user.is_anonymous():
            result['msg'] = "页面已失效，请刷新"
            result['resultcode'] = 1
            return Response(result)

        # 其他终端登录
        session_age = request.session.get_expiry_age()
        session_id = request.session.session_key
        user = User.objects.get(id=request.user.id)
        if user.isonline == 1 and user.sessionid != session_id:
            logout(request)
            result['msg'] = "账户在其他终端上登录，请重新登录!"
            result['resultcode'] = 1

        # session过期
        if util.time_calculator(util.get_current_time(), str(user.last_login)) > session_age:
            result['msg'] = "登录状态过期，请重新登录!"
            result['resultcode'] = 1

        return Response(result)


class CustomChangeAccountPasswordView(ChangeAccountPasswordView):
    change_password_form = CustomPasswordChangeForm


class CustomChangePasswordView(ChangePasswordView):
    change_password_form = CustomAdminPasswordChangeForm
