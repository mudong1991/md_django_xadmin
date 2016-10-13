# coding=utf-8

VERSION = (0, 1, 0)


class Settings(object):
    """
    相关设置
    """
    pass


def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    # 注册所有插件（在apps.py注册了就无需在这里声明）
    # from firstapp.plugins import register_builtin_plugins
    # register_builtin_plugins()
    pass

# loading app config
default_app_config = "firstapp.apps.FirstappConfig"


