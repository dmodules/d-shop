from django.conf.urls import url
from rest_framework.settings import api_settings

from cms.apphook_pool import apphook_pool
from cms.cms_menus import SoftRootCutter
from menus.menu_pool import menu_pool

from shop.cms_apphooks import CatalogListCMSApp, OrderApp, PasswordResetApp
from shop.rest.filters import CMSPagesFilterBackend

class CatalogListApp(CatalogListCMSApp):
  def get_urls(self, page=None, language=None, **kwargs):
    from shop.views.catalog import AddToCartView, ProductListView, ProductRetrieveView
    from shop.views.catalog import AddFilterContextMixin
    from dshop.serializers import AddProductVariableToCartSerializer

    ProductListView = type('ProductSearchListView', (AddFilterContextMixin, ProductListView), {})
    filter_backends = [CMSPagesFilterBackend]
    filter_backends.extend(api_settings.DEFAULT_FILTER_BACKENDS)
    return [
      url(r'^(?P<slug>[\w-]+)/add-to-cart', AddToCartView.as_view()),
      url(r'^(?P<slug>[\w-]+)/add-productvariable-to-cart', AddToCartView.as_view(
        serializer_class=AddProductVariableToCartSerializer,
      )),
      url(r'^(?P<slug>[\w-]+)', ProductRetrieveView.as_view(use_modal_dialog=False)),
      url(r'^', ProductListView.as_view(filter_backends=filter_backends)),
    ]
apphook_pool.register(CatalogListApp)

apphook_pool.register(OrderApp)
apphook_pool.register(PasswordResetApp)

def _deregister_menu_pool_modifier(Modifier):
  index = None
  for k, modifier_class in enumerate(menu_pool.modifiers):
    if issubclass(modifier_class, Modifier):
      index = k
  if index is not None:
    menu_pool.modifiers.pop(index)

_deregister_menu_pool_modifier(SoftRootCutter)