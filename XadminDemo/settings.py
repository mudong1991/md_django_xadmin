# -*- coding: UTF-8 -*-
"""
Django settings for XadminDemo project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import os.path
from django.utils.translation import ugettext, ugettext_lazy as _

reload(sys)
sys.setdefaultencoding('utf-8')
gettext = lambda s: s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'owf60(n97o=b&cvb1$08g$uz75pe77x@w#=ctz0suwccer-=a^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'firstapp',

    'xadmin',
    'crispy_forms',
    'rest_framework',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'firstapp.middleware.CustomAuthorizeMiddleWare',
]

ROOT_URLCONF = 'XadminDemo.urls'

SITE_ID = 1  # 加入了django.contrib.sites需要配置这个

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'XadminDemo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'firstapp.password_validators.CustomMinimumLengthValidator',
    },
    {
        'NAME': 'firstapp.password_validators.CustomUserAttributeSimilarityValidator',
    },
    {
        'NAME': 'firstapp.password_validators.CustomCommonPasswordValidator',
    },
    {
        'NAME': 'firstapp.password_validators.CustomNumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# 翻译文件所在目录，需要手工创建
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
LANGUAGES = [
    ('zh-hans', gettext('Simplified Chinese')),
    ('en', gettext('English')),
]  # xadmin自带的的语言设置插件

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 登录登出url设置
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/'

# 登录锁定设置
LOCK_TIME = 180     # 锁定时间限制(单位是秒)

LOGIN_FAILED_TIMES_LIMIT = 3    # 密码错误限制次数

SESSION_TIME_OUT = 48 * 60 * 60

# session config
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 24 * 60 * 60

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/tmp/django_cache',
#     }
# }

# 自定义用户模型
# AUTH_USER_MODEL = 'firstapp.User'

# xadmin全局设置
XADMIN_VERSION = u'1.2.3.0'
XADMIN_TITLE = _("Educational administration system")
XADMIN_FOOTER_TITLE = _("Shenzhen, the industrial bank  MuDong making - 2016")

# 日志器设置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(MEDIA_ROOT, 'tempfiles', 'logs', 'debug.log')
        },
        'running': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(MEDIA_ROOT, 'tempfiles', 'logs', 'info.log')
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'info': {
            'handlers': ["running"],
            'level': 'INFO',
            'propagate': True
        }
    }
}
