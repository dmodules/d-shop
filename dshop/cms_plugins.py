from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import select_template

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import dmBlocTextMedia
from .models import dmBlocEntete, dmBlocEnteteVideo
from .models import dmBlocSliderParent, dmBlocSliderChild
from .models import dmProductsCategories
from .models import dmProductsVedette, dmProductsByCategory
from .models import dmBlocContact, dmInfolettre
from .models import dmBlocEtapesParent, dmBlocEtapesChild
from .models import dmBlockSalesParent, dmBlockSalesChild
from .models import dmBlockCalltoaction


class BoutiquePlugin(CMSPluginBase):
    module = 'A Boutique Plugin'


#######################################################################
# Plugin: Site
#######################################################################


@plugin_pool.register_plugin
class dmBlocEntetePlugin(BoutiquePlugin):
    name = _("Page's Header")
    model = dmBlocEntete
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocEntetePlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-entete.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-entete.html"
        ])


@plugin_pool.register_plugin
class dmBlocTextMediaPlugin(BoutiquePlugin):
    name = _("Text With Media")
    model = dmBlocTextMedia
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocTextMediaPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-textmedia.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-textmedia.html"
        ])


@plugin_pool.register_plugin
class dmBlocEnteteVideoPlugin(BoutiquePlugin):
    name = _("Header With Video")
    model = dmBlocEnteteVideo
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocEnteteVideoPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-entete-video.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-entete-video.html"
        ])


@plugin_pool.register_plugin
class dmBlocSliderParentPlugin(BoutiquePlugin):
    name = _("Slider")
    model = dmBlocSliderParent
    allow_children = True
    child_classes = ["dmBlocSliderChildPlugin"]

    def render(self, context, instance, placeholder):
        context = super(dmBlocSliderParentPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-slider-parent.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-slider-parent.html"
        ])


@plugin_pool.register_plugin
class dmBlocSliderChildPlugin(BoutiquePlugin):
    name = _("Slider's Element")
    model = dmBlocSliderChild
    allow_children = False
    require_parent = True
    parent_classes = ["dmBlocSliderParentPlugin"]
    fieldsets = [
        (_("Texts"), {
            "fields": [
                ("title", "title_color"),
                ("subtitle", "subtitle_color"),
                "position_text"
            ]
        }), (_("Background"), {
            "fields": [
                "bg_color",
                "image"
            ]
        }),
        (_("Link"), {
            "classes": ("collapse", ),
            "fields": [
                "btn_label",
                "btn_url",
                "btn_blank",
            ]
        })
    ]

    def render(self, context, instance, placeholder):
        context = super(dmBlocSliderChildPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-slider-child.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-slider-child.html"
        ])


@plugin_pool.register_plugin
class dmBlocEtapesParentPlugin(BoutiquePlugin):
    name = _("Steps")
    model = dmBlocEtapesParent
    allow_children = True
    child_classes = ["dmBlocEtapesChildPlugin"]

    def render(self, context, instance, placeholder):
        context = super(dmBlocEtapesParentPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-etapes-parent.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-etapes-parent.html"
        ])


@plugin_pool.register_plugin
class dmBlocEtapesChildPlugin(BoutiquePlugin):
    name = _("Steps's Element")
    model = dmBlocEtapesChild
    allow_children = False
    require_parent = True
    parent_classes = ["dmBlocEtapesParentPlugin"]

    def render(self, context, instance, placeholder):
        context = super(dmBlocEtapesChildPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-etapes-child.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-etapes-child.html"
        ])


@plugin_pool.register_plugin
class dmCalltoactionPlugin(BoutiquePlugin):
    name = _("Call To Action")
    model = dmBlockCalltoaction
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmCalltoactionPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-calltoaction.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-calltoaction.html"
        ])


@plugin_pool.register_plugin
class dmBlocContactPlugin(BoutiquePlugin):
    name = _("Contact Card")
    model = dmBlocContact
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocContactPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-infolettre.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-infolettre.html"
        ])


@plugin_pool.register_plugin
class dmInfolettrePlugin(BoutiquePlugin):
    name = _("Newsletter")
    model = dmInfolettre
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmInfolettrePlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/bloc-infolettre.html".format(
                settings.THEME_SLUG
            ), "plugins/bloc-infolettre.html"
        ])


#######################################################################
# Plugin: Boutique
#######################################################################


@plugin_pool.register_plugin
class dmProductsCategoriesPlugin(BoutiquePlugin):
    name = _("Products Categories")
    model = dmProductsCategories
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsCategoriesPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/products-categories.html".format(
                settings.THEME_SLUG
            ), "plugins/products-categories.html"
        ])


@plugin_pool.register_plugin
class dmProductsVedettePlugin(BoutiquePlugin):
    name = _("Featured Products")
    model = dmProductsVedette
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsVedettePlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/products-vedette.html".format(
                settings.THEME_SLUG
            ), "plugins/products-vedette.html"
        ])


@plugin_pool.register_plugin
class dmProductsByCategpryPlugin(BoutiquePlugin):
    name = _("Products By Category")
    model = dmProductsByCategory
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsByCategpryPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/products-by-category.html".format(
                settings.THEME_SLUG
            ), "plugins/products-by-category.html"
        ])


@plugin_pool.register_plugin
class dmBlockSalesParentPlugin(BoutiquePlugin):
    name = _("Sales")
    model = dmBlockSalesParent
    allow_children = True
    child_classes = ["dmBlockSalesChildPlugin"]

    def render(self, context, instance, placeholder):
        context = super(dmBlockSalesParentPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/block-sales-parent.html".format(
                settings.THEME_SLUG
            ), "plugins/block-sales-parent.html"
        ])


@plugin_pool.register_plugin
class dmBlockSalesChildPlugin(BoutiquePlugin):
    name = _("Sales's Element")
    model = dmBlockSalesChild
    allow_children = False
    require_parent = True
    parent_classes = ["dmBlockSalesParentPlugin"]

    def render(self, context, instance, placeholder):
        context = super(dmBlockSalesChildPlugin, self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            "theme/{}/plugins/block-sales-child.html".format(
                settings.THEME_SLUG
            ), "plugins/block-sales-child.html"
        ])
