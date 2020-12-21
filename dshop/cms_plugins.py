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
    name = _("Entête de page")
    model = dmBlocEntete
    render_template = 'plugins/bloc-entete.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocEntetePlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmBlocTextMediaPlugin(BoutiquePlugin):
    name = _("Bloc Texte avec média")
    model = dmBlocTextMedia
    render_template = 'plugins/bloc-textmedia.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocTextMediaPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmBlocEnteteVideoPlugin(BoutiquePlugin):
    name = _("Bloc d'entête avec vidéo")
    model = dmBlocEnteteVideo
    render_template = 'plugins/bloc-entete-video.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocEnteteVideoPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmBlocSliderParentPlugin(BoutiquePlugin):
    name = _("Bloc slider")
    model = dmBlocSliderParent
    allow_children = True
    child_classes = ['dmBlocSliderChildPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlocSliderParentPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/bloc-slider-parent.html'.format(
                settings.CLIENT_SLUG), 'plugins/bloc-slider-parent.html'
        ])


@plugin_pool.register_plugin
class dmBlocSliderChildPlugin(BoutiquePlugin):
    name = _("Élément du bloc slider")
    model = dmBlocSliderChild
    allow_children = False
    require_parent = True
    parent_classes = ['dmBlocSliderParentPlugin']
    fieldsets = [(_('Textes'), {
        'fields': [('title', 'title_color'), ('subtitle', 'subtitle_color'),
                   'position_text']
    }), (_('Fond'), {
        'fields': ['bg_color', 'image']
    }),
                 (_('Lien'), {
                     'classes': ('collapse', ),
                     'fields': [
                         'btn_label',
                         'btn_url',
                         'btn_blank',
                     ]
                 })]

    def render(self, context, instance, placeholder):
        context = super(dmBlocSliderChildPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/bloc-slider-child.html'.format(
                settings.CLIENT_SLUG), 'plugins/bloc-slider-child.html'
        ])


@plugin_pool.register_plugin
class dmBlocEtapesParentPlugin(BoutiquePlugin):
    name = _("Bloc d'étapes")
    model = dmBlocEtapesParent
    render_template = 'plugins/bloc-etapes-parent.html'
    allow_children = True
    child_classes = ['dmBlocEtapesChildPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlocEtapesParentPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmBlocEtapesChildPlugin(BoutiquePlugin):
    name = _("Élément du bloc d'étapes")
    model = dmBlocEtapesChild
    render_template = 'plugins/bloc-etapes-child.html'
    allow_children = False
    require_parent = True
    parent_classes = ['dmBlocEtapesParentPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlocEtapesChildPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmCalltoactionPlugin(BoutiquePlugin):
    name = _("Bloc call to action")
    model = dmBlockCalltoaction
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmCalltoactionPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/bloc-calltoaction.html'.format(
                settings.CLIENT_SLUG), 'plugins/bloc-calltoaction.html'
        ])


@plugin_pool.register_plugin
class dmBlocContactPlugin(BoutiquePlugin):
    name = _("Bloc contact")
    model = dmBlocContact
    render_template = 'plugins/bloc-contact.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmBlocContactPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmInfolettrePlugin(BoutiquePlugin):
    name = _("Bloc infolettre")
    model = dmInfolettre
    render_template = 'plugins/bloc-infolettre.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmInfolettrePlugin,
                        self).render(context, instance, placeholder)
        return context


#######################################################################
# Plugin: Boutique
#######################################################################


@plugin_pool.register_plugin
class dmProductsCategoriesPlugin(BoutiquePlugin):
    name = _("Catégories de produit")
    model = dmProductsCategories
    render_template = 'plugins/products-categories.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsCategoriesPlugin,
                        self).render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class dmProductsVedettePlugin(BoutiquePlugin):
    name = _("Produits Vedette")
    model = dmProductsVedette
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsVedettePlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/products-vedette.html'.format(
                settings.CLIENT_SLUG), 'plugins/products-vedette.html'
        ])


@plugin_pool.register_plugin
class dmProductsByCategpryPlugin(BoutiquePlugin):
    name = _("Produits par catégorie")
    model = dmProductsByCategory
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super(dmProductsByCategpryPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/products-by-category.html'.format(
                settings.CLIENT_SLUG), 'plugins/products-by-category.html'
        ])


@plugin_pool.register_plugin
class dmBlockSalesParentPlugin(BoutiquePlugin):
    name = _("Bloc vente")
    model = dmBlockSalesParent
    allow_children = True
    child_classes = ['dmBlockSalesChildPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlockSalesParentPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/block-sales-parent.html'.format(
                settings.CLIENT_SLUG), 'plugins/block-sales-parent.html'
        ])


@plugin_pool.register_plugin
class dmBlockSalesChildPlugin(BoutiquePlugin):
    name = _("Élément du bloc vente")
    model = dmBlockSalesChild
    allow_children = False
    require_parent = True
    parent_classes = ['dmBlockSalesParentPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlockSalesChildPlugin,
                        self).render(context, instance, placeholder)
        return context

    def get_render_template(self, context, instance, placeholder):
        return select_template([
            '/app/apps/dmTheme/templates/{}/plugins/block-sales-child.html'.format(
                settings.CLIENT_SLUG), 'plugins/block-sales-child.html'
        ])
