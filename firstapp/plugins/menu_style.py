# -*- coding: UTF-8 -*-
__author__ = 'MD'
from firstapp.util import cust_html
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView

BUILDIN_STYLES = {
    'cust_accordion': cust_html("cust_menu"),
}


class SiteMenuStylePlugin(BaseAdminPlugin):

    cust_menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.cust_menu_style) and self.cust_menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.cust_menu_style]
        return context

site.register_plugin(SiteMenuStylePlugin, CommAdminView)


