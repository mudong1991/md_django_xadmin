# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.sites import site


class ListViewInitPlugin(BaseAdminPlugin):
    # 添加媒体文件
    def get_media(self, media):
        media.add_css({"screen": ["js/imgviewers/viewer.css", ]})
        media.add_js(["js/imgviewers/viewer.js", "js/cust_listview.js",])
        return media

site.register_plugin(ListViewInitPlugin, ListAdminView)