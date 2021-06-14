from django.conf.urls import url

from cms.apphook_pool import apphook_pool
from cms.cms_menus import SoftRootCutter
from menus.menu_pool import menu_pool

from shop.cms_apphooks import CatalogListCMSApp, OrderApp, PasswordResetApp
from dshop.views import DshopProductListView, OrderView


class CatalogListApp(CatalogListCMSApp):
    """
    Create a useable list of urls with Product's slug.
    """
    def get_urls(self, page=None, language=None, **kwargs):
        from dshop.catalog import AddToCartView
        from dshop.catalog import ProductRetrieveView
        from dshop.serializers import AddProductVariableToCartSerializer

        return [
            # Product loading page
            url(
                r'^category/(?P<category_id>[0-9]+)-(?P<category_slug>.+)$',
                DshopProductListView.as_view(),
            ),
            url(
                r'^brand/(?P<brand_id>[0-9]+)-(?P<brand_slug>.+)$',
                DshopProductListView.as_view(),
            ),
            url(
                r'^(?P<slug>[\w-]+)/add-to-cart',
                AddToCartView.as_view(), name="add_to_cart"
            ),
            url(
                r'^(?P<slug>[\w-]+)/add-productvariable-to-cart',
                AddToCartView.as_view(
                    serializer_class=AddProductVariableToCartSerializer,
                ), name="add_productvariable_to_cart"
            ),
            url(
                r'^(?P<slug>[\w-]+)',
                ProductRetrieveView.as_view(use_modal_dialog=False)
            ),
            url(
                r'^',
                DshopProductListView.as_view(),
                name='produits'
            ),
        ]


class OrderApp(OrderApp):

    def get_urls(self, page=None, language=None, **kwargs):
        from django.conf.urls import url

        return [
            url(r'^(?P<slug>[\w-]+)/(?P<secret>[\w-]+)',
                OrderView.as_view(many=False)),  # publicly accessible
            url(r'^(?P<slug>[\w-]+)',
                OrderView.as_view(many=False)),  # requires authentication
            url(r'^',
                OrderView.as_view()),  # requires authentication
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
