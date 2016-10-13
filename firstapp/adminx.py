# -*- coding: UTF-8 -*-
__author__ = 'MD'

from xadmin.sites import site
from firstapp.admins import (ModelAdmins, AuthAdmins)
from firstapp.xadmin_views import *
from xadmin.views import IndexView
from xadmin.plugins import quickform

# 设置xadmin初始化注册的一些东西
copy_register_list = site.copy_registry()

# 移除账户密码修改视图
copy_register_list['views'].remove(('^account/password/$', ChangeAccountPasswordView, 'account_password'))
copy_register_list['views'].remove(('^auth/user/(.+)/update/password/$', ChangePasswordView,
                                    'user_change_password'))
# 移除quickform插件，重新自定义
copy_register_list['plugins'][ModelFormAdminView].remove(quickform.QuickFormPlugin)
copy_register_list['plugins'][ModelFormAdminView].remove(quickform.QuickAddBtnPlugin)

site.restore_registry(copy_register_list)

########################################################################################################################

# 基础视图设置注册
site.register(BaseAdminView, BaseViewSetting)

# 登录页注册设置
site.register(LoginView, LoginViewSetting)

# 退出视图注册设置
site.register(LogoutView, LogoutViewSetting)

# 全局注册（用户登录认证后的的公共页）
site.register(CommAdminView, CommonViewSetting)

# 列表页注册（列出数据的页面）
site.register(ListAdminView, ListPageViewSetting)

# 模型数据表单页面
site.register(ModelFormAdminView, ModelFormAdminViewSetting)

########################################################################################################################

################
# 数据模型注册 #
################

# 用户注册
site.unregister(User)
site.register(User, AuthAdmins.CustUserAdmin)

# 用户权限重新注册
site.unregister(Permission)
site.register(Permission, AuthAdmins.CustPerssionAdmin)

# 用户组重新注册
site.unregister(Group)
site.register(Group, AuthAdmins.CustGroupAdmin)

# 用户日志注册
site.register(models.UserLogs, ModelAdmins.UserLogsAdmin)

# 告警日志注册
site.register(models.WarningLogs, ModelAdmins.WarningLogsAdmin)

# 图书注册
site.register(models.Book, ModelAdmins.BookAdmin)


site.register(models.BookCategory, ModelAdmins.BookCategory)


##################
# 自定义视图注册 #
##################

# 修改账户密码修改路由配置

site.register_view(r'^account/password/$', CustomChangeAccountPasswordView, name='account_password')
site.register_view(r'^auth/user/(.+)/update/password/$', CustomChangePasswordView, name='user_change_password')

# 自定义主页
site.register_view(r'^index/$', IndexView, name='custom_index')

# 运行状态页面的路由配置
site.register_view(r'^running/$', RunningView, name='running')
site.register_view(r'^running_content/$', RunningContentView, name='running_content')

