# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
import django.utils.timezone as timezone


# Create your models here.
def get_error_messages(label):
    return {
        "blank": "{0}: 不能为空！".format(label),
        "unique": "{0}: 已经存在！".format(label),
        "max_length": "{0}:长度超过指定范围！".format(label)
    }


class ProfileBase(type):  # 对于传统类，他们的元类都是types.ClassType
    def __new__(cls, name, bases, attrs):  # 带参数的构造器，__new__一般用于设置不变数据类型的子类
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)


class ProfileUser(object):
    __metaclass__ = ProfileBase  # 类属性


# 用户模型
class MyProfile(ProfileUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.jpg',
                               max_length=200, blank=True, null=True, verbose_name=_("avatar"))
    qq = models.CharField(default='', max_length=20, null=True, blank=True, verbose_name=_('QQ number'))
    mobile = models.CharField(default='', max_length=11, blank=True, null=True, verbose_name=_('mobile'))
    url = models.CharField(default='', max_length=100, blank=True, null=True, verbose_name=_('Personal url'))
    sessionid = models.CharField(default="", max_length=255, blank=True, null=True, verbose_name=_('session'))
    isonline = models.BooleanField(default=False, verbose_name=_("online"))
    login_times = models.IntegerField(default=0, verbose_name=_("login times"))  # 登录过的次数

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.username


class UserLogs(models.Model):
    """
    用户日志
    """
    operation_type_choice = (
        (1, _('login/logout')),
        (2, _("other"))
    )
    operation_result = {'login_success': _('login successful'), 'logout_success': _('logout successful')}

    user = models.ForeignKey(User, verbose_name=_('username'))
    ip = models.CharField(max_length=255, verbose_name=_('IP'))
    operation_type = models.IntegerField(blank=True, null=True, verbose_name=_('operation type'),
                                         choices=operation_type_choice)
    read = models.BooleanField(default=False, verbose_name=_('read over'))
    time = models.DateTimeField(max_length=255, default=timezone.now, blank=True, verbose_name=_('time'))
    description = models.CharField(default='', max_length=500, verbose_name=_('description'))

    class Meta:
        verbose_name = _('user log')
        verbose_name_plural = _('user logs')
        db_table = "userlogs"
        ordering = ('-time',)
        default_permissions = ('view', 'change', 'add', 'delete')

    def __unicode__(self):
        return self.user.username


class UserLoginLogs(models.Model):
    """
    用户登录日志
    """
    username = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    status = models.IntegerField()
    login_time = models.CharField(max_length=255)

    class Meta:
        db_table = "userloginlogs"
        ordering = ('-login_time',)
        default_permissions = []


class LockIp(models.Model):
    """
    锁定的IP
    """
    ip = models.CharField(max_length=255)
    lock_time = models.CharField(max_length=255)

    class Meta:
        db_table = "lockip"
        default_permissions = []


class SystemStatus(models.Model):
    """
    系统状态
    """
    cur_system_version = models.CharField(max_length=255, blank=True, default="0.1.1.0")

    def get_cur_system_time(self):
        """
        Method to get current time
        """
        import time

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    class Meta:
        verbose_name = _("system status")
        verbose_name_plural = verbose_name
        ordering = ('-id',)
        db_table = 'systemstatus'
        default_permissions = ("view", "change", "add", "delete")


class WarningLogs(models.Model):
    """
    告警日志
    """
    warning_type_choice = (
        (0, _('unknown')),
        (1, _('system exception')),
        (2, _('network exception'))
    )
    serious_level_choice = (
        (0, _('unknown')),
        (1, _('slight')),
        (2, _('general')),
        (3, _('serious')),
    )
    device_ip = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name=_('IP'))
    warning_type = models.IntegerField(default=0, blank=True, choices=warning_type_choice,
                                       verbose_name=_('warning type'))
    serious_level = models.IntegerField(default=0, blank=True, choices=serious_level_choice,
                                        verbose_name=_('serious level'))
    description = models.CharField(default="", blank=True, max_length=2048, verbose_name=_('description'))
    read_flag = models.BooleanField(default=False, blank=True, verbose_name=_("read over"))
    happen_time = models.DateTimeField(default=timezone.now, blank=True, max_length=255, verbose_name=_('happened time'))
    extra = models.CharField(default="", blank=True, max_length=255, verbose_name=_('extraneous information'))

    class Meta:
        verbose_name = _('warning log')
        verbose_name_plural = _('warning logs')
        db_table = "warninglogs"
        ordering = ('read_flag', '-happen_time')
        default_permissions = ("view", "change", "add", "delete")

    def __unicode__(self):
        return self.device_ip


class BookCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Book Categories"))
    ordering = models.IntegerField(blank=True, null=True, verbose_name=_("ordering"))

    class Meta:
        verbose_name = _('Book Category')
        verbose_name_plural = _('Book Categories')
        db_table = 'bookcategory'
        ordering = ('ordering',)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    source_choice = (
        (0, _("purchase")),
        (1, _("borrowed")),
        (2, _("present"))
    )
    # 基本信息
    number = models.CharField(max_length=500, unique=True, verbose_name=_("number"),
                              help_text=_("Serial number must be unique"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    author = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Author'))
    category = models.ManyToManyField(BookCategory, verbose_name=_("category"), blank=True,
                                      help_text=_("Add the classification of the books "), related_name="user_set")
    image = models.ImageField(upload_to='book/%Y/%m', max_length=200, blank=True, null=True, verbose_name=_("image"))
    page = models.SmallIntegerField(blank=True, null=True, verbose_name=_("page"))
    book_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("book number"))
    price = models.FloatField(verbose_name=_('price'), blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True, verbose_name=_("publish time"))
    publish_house = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("publish house"))
    note = models.CharField(max_length=2048, blank=True, null=True, verbose_name=_("note"))

    # 入库信息
    source = models.IntegerField(default=0, blank=True, null=True, choices=source_choice,verbose_name=_("source"))
    storage_time = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name=_("storage time"))
    inventory = models.IntegerField(blank=True, null=True, verbose_name=_('inventory'))
    borrowing_times = models.IntegerField(default=0, blank=True, null=True,verbose_name=_("borrowing times"))

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _("books")
        ordering = ("number",)
        db_table = 'book'

    def __unicode__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _("students")
        ordering = ("id",)
        db_table = 'student'

    def __unicode__(self):
        return self.name


class BookBorrowInfo(models.Model):
    status_choice = (
        (0, _("borrow")),
        (1, _("return")),
        (2, _("unknown"))
    )

    book = models.ForeignKey(Book)
    student = models.ForeignKey(Student)
    borrow_time = models.DateTimeField(default=timezone.now)
    standard_return_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=3))
    real_return_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choice, default=0)

    class Meta:
        verbose_name = _("bookborrowinfo")
        verbose_name_plural = _("bookborrowinfos")
        db_table = "bookborrowinfo"
