# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, BaseAdminView, CommAdminView
from firstapp.util import cust_img


class SiteIconPlugin(BaseAdminPlugin):
    site_icon = None

    def init_request(self, *args, **kwargs):
        return bool(self.site_icon)

    def block_extrahead(self, context, nodes):
        if self.site_icon:
            nodes.append("<link rel='icon' type='image/x-icon' href='{0}' />".format(
                self.static(cust_img(self.site_icon))))

site.register_plugin(SiteIconPlugin, BaseAdminView)

