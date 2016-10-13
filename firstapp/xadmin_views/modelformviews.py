# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views import ModelFormAdminView


class ModelFormAdminViewSetting(ModelFormAdminView):
    def get_media(self):
        return super(ModelFormAdminView, self).get_media() + self.form_obj.media + \
               self.vendor('xadmin.form.css')
