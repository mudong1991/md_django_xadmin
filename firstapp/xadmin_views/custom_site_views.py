# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views.base import BaseAdminView, CommAdminView, ModelAdminView
from firstapp.util import cust_html
from django.utils.translation import ugettext_lazy as _


class RunningView(CommAdminView):
    need_site_permission = True  # 是否需要站点认证权限

    def get(self, request, *args, **kwargs):
        context = super(RunningView, self).get_context()
        context.update({"title": '系统状态'})
        context["breadcrumbs"].append({"url": '/running/', 'title': _('System running status')})
        return self.template_response(cust_html('running'), context=context)


class RunningContentView(BaseAdminView):
    need_site_permission = True

    def get(self, request, *args, **kwargs):
        context = super(RunningContentView, self).get_context()
        context.update({"title": '系统状态'})
        return self.template_response(cust_html('running_content'), context=context)
