# -*- coding: UTF-8 -*-
__author__ = 'MD'
from firstapp.models import *
import threading
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext, ugettext_lazy as _


def handle_permission():
    # 权限初始化
    Permission.objects.filter(codename__contains='lockip').delete()
    Permission.objects.filter(codename__contains='loginlogs').delete()
    if 'django.contrib.contenttypes' in settings.INSTALLED_APPS:
        Permission.objects.filter(codename__contains='contenttype').delete()
    if 'django.contrib.sessions' in settings.INSTALLED_APPS:
        Permission.objects.filter(codename__contains='session').delete()
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        Permission.objects.filter(codename__contains='site').delete()


def init():
    """
    初始化数据
    :return:
    """
    # 初始化权限
    handle_permission()

    # 判断是否已经初始化了
    user_count = User.objects.count()
    if user_count:
        return

    # 填充系统版本信息
    SystemStatus.objects.create(cur_system_version=settings.XADMIN_VERSION)
    # 初始化用户
    admin = User.objects.create(username='admin', password=make_password('123456'), is_superuser=1, is_staff=1)
    # 初始化用户组
    admin_group = Group.objects.create(name='administrator')
    # 加入组和权限
    admin.groups.add(admin_group)


def thread_init(sender, **kwargs):
    """
        第一个参数必须是sender，且必须有kwargs参数

        :param sender:
        :param kwargs:
        :return:
        """

    # 在另一个线程中执行init方法，主要是为了解决数据库事务提交延迟的问题。
    t = threading.Timer(1, init)

    t.start()
