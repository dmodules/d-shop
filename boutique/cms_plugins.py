from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import dmBlocEntete, dmBlocTextMedia, dmBlocEnteteVideo, dmBlocSliderParent, dmBlocSliderChild, dmProductsCategories, dmProductsVedette, dmBlocContact, dmInfolettre, dmBlocEtapesParent, dmBlocEtapesChild

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
    context = super(dmBlocEntetePlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmBlocTextMediaPlugin(BoutiquePlugin):
  name = _("Bloc Texte avec média")
  model = dmBlocTextMedia
  render_template = 'plugins/bloc-textmedia.html'
  allow_children = False

  def render(self, context, instance, placeholder):
    context = super(dmBlocTextMediaPlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmBlocEnteteVideoPlugin(BoutiquePlugin):
  name = _("Bloc d'entête avec vidéo")
  model = dmBlocEnteteVideo
  render_template = 'plugins/bloc-entete-video.html'
  allow_children = False

  def render(self, context, instance, placeholder):
    context = super(dmBlocEnteteVideoPlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmBlocSliderParentPlugin(BoutiquePlugin):
  name = _("Bloc slider")
  model = dmBlocSliderParent
  render_template = 'plugins/bloc-slider-parent.html'
  allow_children = True
  child_classes = ['dmBlocSliderChildPlugin']

  def render(self, context, instance, placeholder):
    context = super(dmBlocSliderParentPlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmBlocSliderChildPlugin(BoutiquePlugin):
    name = _("Élément du bloc slider")
    model = dmBlocSliderChild
    render_template = 'plugins/bloc-slider-child.html'
    allow_children = False
    require_parent = True
    parent_classes = ['dmBlocSliderParentPlugin']

    def render(self, context, instance, placeholder):
        context = super(dmBlocSliderChildPlugin, self).render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class dmBlocEtapesParentPlugin(BoutiquePlugin):
  name = _("Bloc d'étapes")
  model = dmBlocEtapesParent
  render_template = 'plugins/bloc-etapes-parent.html'
  allow_children = True
  child_classes = ['dmBlocEtapesChildPlugin']

  def render(self, context, instance, placeholder):
    context = super(dmBlocEtapesParentPlugin, self).render(context, instance, placeholder)
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
        context = super(dmBlocEtapesChildPlugin, self).render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class dmBlocContactPlugin(BoutiquePlugin):
  name = _("Bloc contact")
  model = dmBlocContact
  render_template = 'plugins/bloc-contact.html'
  allow_children = False

  def render(self, context, instance, placeholder):
    context = super(dmBlocContactPlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmInfolettrePlugin(BoutiquePlugin):
  name = _("Bloc infolettre")
  model = dmInfolettre
  render_template = 'plugins/bloc-infolettre.html'
  allow_children = False

  def render(self, context, instance, placeholder):
    context = super(dmInfolettrePlugin, self).render(context, instance, placeholder)
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
    context = super(dmProductsCategoriesPlugin, self).render(context, instance, placeholder)
    return context

@plugin_pool.register_plugin
class dmProductsVedettePlugin(BoutiquePlugin):
  name = _("Produits Vedette")
  model = dmProductsVedette
  render_template = 'plugins/products-vedette.html'
  allow_children = False

  def render(self, context, instance, placeholder):
    context = super(dmProductsVedettePlugin, self).render(context, instance, placeholder)
    return context