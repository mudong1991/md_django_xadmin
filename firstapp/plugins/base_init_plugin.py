# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, BaseAdminView
from firstapp import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class InitPlugin(BaseAdminPlugin):
    is_init = False

    def init_request(self, *args, **kwargs):
        return bool(self.is_init)

    def get_context(self, context):
        current_veresion = models.SystemStatus.objects.first().cur_system_version
        site_title = getattr(settings, "XADMIN_TITLE", _(u"Django Xadmin"))
        site_footer = getattr(settings, "XADMIN_FOOTER_TITLE", _(u"my-company.inc"))
        context.update({"current_version": current_veresion, 'site_title': site_title,
                        'site_footer': site_footer})
        context["LANGUAGE_CODE"] = self.request.LANGUAGE_CODE
        context["LANGUAGES"] = settings.LANGUAGES
        return context


site.register_plugin(InitPlugin, BaseAdminView)
