# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views import BaseAdminPlugin, CommAdminView
from xadmin.sites import site


class CommonInitPlugin(BaseAdminPlugin):

    # 添加媒体文件
    def get_media(self, media):
        media.add_css({"screen": ["css/cust_index.css", "css/font-awesome.min.css"]})
        return media

site.register_plugin(CommonInitPlugin, CommAdminView)
