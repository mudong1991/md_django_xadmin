# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class FirstappConfig(AppConfig):
    name = 'firstapp'

    def ready(self):
        # 注册所有插件
        from firstapp.plugins import register_builtin_plugins
        register_builtin_plugins()

        # 初始化用户和权限
        from firstapp.init_data import thread_init  # 最好是在ready方法内再引入models.py
        post_migrate.connect(receiver=thread_init, sender=self)
