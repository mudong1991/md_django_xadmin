# -*- coding: UTF-8 -*-
__author__ = 'MD'
from django.template import loader
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView
from firstapp.models import SystemStatus


class TimerPlugin(BaseAdminPlugin):
    show_time = False

    def init_request(self, *args, **kwargs):
        return bool(self.show_time)

    def block_top_navmenu(self, context, nodes):
        context.update({"system_time": SystemStatus().get_cur_system_time()})
        nodes.append(loader.render_to_string('firstapp/blocks/timer.html', get_context_dict(context)))

site.register_plugin(TimerPlugin, CommAdminView)
