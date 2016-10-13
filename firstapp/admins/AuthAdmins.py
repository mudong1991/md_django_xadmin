# -*- coding: UTF-8 -*-
__author__ = 'MD'
from firstapp.forms import *
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelMultipleChoiceField
from django.utils.html import format_html
from django.conf import settings


ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


def get_permission_name(p):
    action = p.codename.split('_')[0]
    if action in ACTION_NAME:
        return ACTION_NAME[action] % str(p.content_type)
    else:
        return p.name


class PermissionModelMultipleChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, p):
        return get_permission_name(p)


class CustUserAdmin(object):
    """
    自定义用户管理(根据UserAdmin作了修改)
    """
    list_display = ('username', 'get_avatar', 'email', 'qq', 'mobile', 'url', 'is_active', 'login_times')
    list_filter = ('username', 'email', 'qq', 'mobile', 'is_superuser', 'is_active', 'login_times')
    search_fields = ('username', 'email', 'qq', 'mobile', 'is_superuser', 'is_active')
    ordering = ('username',)

    # 显示字段详情定义
    show_detail_fields = ['username']
    # 编辑字段项定义
    list_editable = ['username']

    change_user_password_template = None
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_avatar(self, user):
        html_str = format_html('<img style="max-width:60px; max-height:80px" src="{}"+/>', settings.MEDIA_URL +
                               str(user.avatar))
        return html_str

    get_avatar.short_description = _("avatar")
    get_avatar.allow_tags = True
    get_avatar.admin_order_field = 'avatar.username'

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(CustUserAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'user_permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = CustomUserCreationForm
        else:
            self.form = CustomUserChangeForm
        return super(CustUserAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(CustUserAdmin, self).get_form_layout()


class CustPerssionAdmin(object):
    def show_name(self, p):
        return get_permission_name(p)

    show_name.short_description = _('Permission Name')
    show_name.is_column = True

    model_icon = 'fa fa-lock'
    list_display = ('show_name',)


class CustGroupAdmin(object):
    search_fields = ('name',)
    ordering = ('name',)
    style_fields = {'permissions': 'm2m_transfer'}
    model_icon = 'fa fa-group'

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(CustGroupAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs
