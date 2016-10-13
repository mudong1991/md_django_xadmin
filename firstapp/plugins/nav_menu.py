# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView


class NavMenuPlugin(BaseAdminPlugin):
    nav_menu = []

    def init_request(self, *args, **kwargs):
        return bool(self.nav_menu)

    def get_context(self, context):
        context["nav_menu"] = self.nav_menu
        return context

site.register_plugin(NavMenuPlugin, CommAdminView)
