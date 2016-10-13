# coding:utf-8
from firstapp.forms import *
from xadmin.layout import Fieldset, Main, Side, Row, FormHelper
from django.utils.translation import ugettext_lazy as _, ungettext
from firstapp.models import *
from django.conf import settings
from django.template import loader
from firstapp.util import cust_html
from xadmin.plugins.utils import get_context_dict


class UserLogsAdmin(object):
    """
    自定义用户日志管理
    """

    # 模型菜单图标
    model_icon = 'fa fa-eye'
    list_display = ('user', 'ip', 'operation_type', 'time', 'get_description', 'read')
    list_filter = ('user', 'ip', 'operation_type', 'time', 'read')
    search_fields = ('user__username', 'ip', 'time', 'get_description', 'read')
    actions = ["read_log"]
    relate_obj = [User]

    # 显示字段详情定义
    show_detail_fields = ['get_description']

    def get_actions(self):
        actions = super(UserLogs, self).get_actions()
        if not self.user.has_perm("userlogs.read_userlogs"):
            if 'read_log' in actions:
                actions.pop('read_log')

    def get_description(self, userlogs):
        description = userlogs.description
        description_list = description.split("|")
        trans_description = ungettext('User %(user)s@%(ip)s operating the %(operation)s, the result is %(result)s',
                                      'User %(user)s@%(ip)s operating the %(operation)s, the result is %(result)s',
                                      description)
        trans_description_format = trans_description % {
            "user": description_list[0],
            'ip': description_list[1],
            'operation': _(description_list[2]),
            'result': _(description_list[3])
        }
        return trans_description_format

    get_description.short_description = _("description")
    get_description.is_column = True
    get_description.allow_tags = True
    get_description.admin_order_field = 'description'

    def read_log(self, request, queryset):
        n_comments = 0
        for comment in queryset:
            comment.read = True
            comment.save()
            n_comments += 1

        msg = ungettext('1 comment was successfully %(action)s.',
                        '%(count)s comments were successfully %(action)s.',
                        n_comments)
        self.message_user(msg % {'count': n_comments, 'action': ungettext('read', 'read', n_comments)}, 'success')

    read_log.short_description = _('Read selected %(verbose_name_plural)s')
    read_log.icon = 'fa fa-pencil'


class WarningLogsAdmin(object):
    """
    告警日志管理
    """
    # 模型菜单图标
    model_icon = 'fa fa-bell'
    list_display = ('device_ip', 'warning_type', 'serious_level', 'happen_time', 'read_flag', 'description', 'extra')
    list_filter = ('device_ip', 'warning_type', 'serious_level', 'happen_time', 'read_flag', 'description')
    search_fields = ('device_ip', 'warning_type', 'description', 'happen_time', 'extra')
    actions = ["read_log"]

    # 显示字段详情定义
    show_detail_fields = ['device_ip']
    # 编辑字段项定义
    # list_editable = ['device_ip']

    def get_actions(self):
        actions = super(WarningLogsAdmin, self).get_actions()
        if not self.user.has_perm("warninglogs.read_warninglogs"):
            if 'read_log' in actions:
                actions.pop('read_log')

    def read_log(self, request, queryset):
        n_wlogs = 0
        for wlog in queryset:
            wlog.read_flag = True
            wlog.save()
            n_wlogs += 1

        msg = ungettext('1 warning log was successfully %(action)s.',
                        '%(count)s warning logs were successfully %(action)s.',
                        n_wlogs)
        self.message_user(msg % {'count': n_wlogs, 'action': ungettext('read', 'read', n_wlogs)}, 'success')

    read_log.short_description = _('Read selected %(verbose_name_plural)s')
    read_log.icon = 'fa fa-pencil'


class BookAdmin(object):
    """
    图书管理
    """
    # 模型菜单图标
    model_icon = 'fa fa-book'
    list_display = ('number', 'name', 'get_image', 'category', 'source', 'storage_time',
                    'inventory', 'borrowing_times', 'price')

    list_filter = ('number', 'name', 'category', 'source', 'storage_time',
                   'inventory', 'borrowing_times', 'price')
    search_fields = ('name', 'author', 'publish_house')

    cust_aggregate_fields = {"inventory": 'sum', 'number': 'count', 'borrowing_times': 'sum', 'price': 'sum'}


    # 显示字段详情定义
    show_detail_fields = ['name']

    # 编辑字段项定义
    list_editable = ['name']

    # data_charts = {
    #     'inventory': {"title": 'Inventory', 'x-field': 'price', 'y-field': 'inventory', 'oder': ("price",)}
    # }

    def get_image(self, book):
        html_str = format_html('<img style="max-width:60px; max-height:80px" src="{}"+/>', settings.MEDIA_URL +
                               str(book.image))
        return html_str

    get_image.short_description = _("image")
    get_image.allow_tags = True
    get_image.admin_order_field = 'image'

    form_layout = (
        Main(
             Fieldset(_("Basic information"),
                      'number',
                      'name',
                      'image',
                      'category',
             ),
             Fieldset(_("Book information"),
                      'author',
                      'publish_time',
                      'publish_house',
                      'book_number',
                      'page',
                      'price'
             )
        ),
        Side(
            Fieldset(_("Inventory information"),
                     'source', 'inventory'
                     )
        )
    )

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = BookCreateForm
        else:
            self.form = BookCreateForm
        return super(BookAdmin, self).get_model_form(**kwargs)

    # Block Views
    def block_form_bottom(self, context, nodes):
        nodes.append(loader.render_to_string(cust_html("book_relate_info"), context=get_context_dict(context)))


class BookCategory(object):
    pass
