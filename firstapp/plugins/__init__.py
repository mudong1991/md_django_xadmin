# -*- coding: UTF-8 -*-
__author__ = 'MD'

PLUGINS = (
    'base_init_plugin',
    'common_init_plugin',
    'listview_init_plugin',
    'menu_style',
    'site_icon',
    'nav_menu',
    'show_time',
    'custom_aggregation',
    'custom_quick_form',
)


def register_builtin_plugins():
    from importlib import import_module
    from django.conf import settings

    exclude_plugins = getattr(settings, 'FIRSTAPP_EXCLUDE_PLUGINS', [])

    [import_module('firstapp.plugins.%s' % plugin) for plugin in PLUGINS if plugin not in exclude_plugins]
