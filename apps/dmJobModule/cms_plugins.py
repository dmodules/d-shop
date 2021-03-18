from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import select_template

from cms.plugin_pool import plugin_pool

from dshop.cms_plugins import BoutiquePlugin

from .models import dmJobLastest


#######################################################################
# Plugin: Site
#######################################################################


@plugin_pool.register_plugin
class dmJobLastestPlugin(BoutiquePlugin):
    name = _("Last Job Offers")
    model = dmJobLastest
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmJobLastestPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-dmjob-lastest.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-dmjob-lastest.html"
        ])
