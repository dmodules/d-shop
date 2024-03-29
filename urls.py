import os

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.views.static import serve
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static

from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from cms.sitemaps import CMSSitemap
from dshop.sitemap import ProductSitemap
from shop.forms.auth import RegisterUserForm
from shop.views.catalog import ProductListView

from dshop.views import CustomerView, CustomerCheckView
from dshop.views import LoadProduits, LoadProductsByCategory
from dshop.views import LoadVariantSelect, LoadFilters
from dshop.views import ShippingMethodsView, BillingMethodsView
from dshop.views import AttributeAutocomplete
from dshop.views import PasswordResetConfirmView, DshopAuthFormView
from dshop.views import unclone_customers, send_queued_mail


def trigger_error(request):
    division_by_zero = 1 / 0 # noqa


sitemaps = {"cmspages": CMSSitemap, "products": ProductSitemap}


def render_robots(request):
    permission = "noindex" in settings.ROBOTS_META_TAGS and "Disallow" or "Allow" # noqa
    return HttpResponse("User-Agent: *\n%s: /\n" % permission, content_type="text/plain") # noqa


admin.site.site_header = _('D-Shop - E-commerce platform')


path_to_extended = '/app/extended_apps/'
EXTENDED_APP_DIR = 'extended_apps'
extended_urls = []
if os.path.exists(path_to_extended):
    for item in os.listdir(path_to_extended):
        app_path = os.path.join(path_to_extended, item)

        if os.path.isdir(app_path):
            inc_url = ".".join([EXTENDED_APP_DIR, str(item), 'urls'])
            new_url = url(r'^'+item+'/', include(inc_url))
            extended_urls.append(new_url)


urlpatterns = [

    url(
        r'^attribute-autocomplete/$',
        AttributeAutocomplete.as_view(), name='attribute-autocomplete'
    ),
    url(r'^robots\.txt$', render_robots),
    url(r'^sitemap\.xml$', sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    url(r'^shop/', include("shop.urls")),
    url(
        r'^dshop/auth/register/',
        DshopAuthFormView.as_view(form_class=RegisterUserForm)
    ),
    url(
        r'^shop/auth/password/reset-confirm/',
        PasswordResetConfirmView.as_view()
    ),
    url(r'^billing-stripe/', include("apps.dmBillingStripe.urls")),
    url(r'^billing-square/', include("apps.dmBillingSquare.urls")),
    url(r'^dm-square/', include("apps.dmSquare.urls")),
    url(r'^contact/', include("apps.dmContact.urls")),
    url(r'^discount/', include("apps.dmRabais.urls")),
    url(r'^quotation/', include("apps.dmQuotation.urls")),
    url(r'^shipping/', include("apps.dmShipping.urls")),

    url(r'^dm-admin/', include("apps.dmAdminTheme.urls")),

    url(
        r'^api/v1/products-list/$',
        ProductListView.as_view(), name='product-list'
    ),
    # =====================
    # url(r'^api/v1/d-shop-products-list/$', DshopProductListView.as_view(), name='d-shop-product-list'), # noqa
    # url(r'^api/v1/d-shop-products-list/category/(?P<category_id>[0-9]+)-(?P<category_slug>.+)$', DshopProductListView.as_view(), name='d-shop-product-list'), # noqa
    # url(r'^api/v1/d-shop-products-list/brand/(?P<brand_id>[0-9]+)-(?P<brand_slug>.+)$', DshopProductListView.as_view(), name='d-shop-product-list'), # noqa
    # =====================
    url(
        r'^api/v1/filters/$',
        LoadFilters.as_view(), name='product-filter'
    ),
    url(
        r'^api/fe/customer/$',
        CustomerView.as_view(), name='customer'
    ),
    url(
        r'^api/fe/customer-check/$',
        CustomerCheckView.as_view(), name="customer-check"
    ),
    url(
        r'^api/fe/moreproduits/$',
        LoadProduits.as_view(), name='moreproducts'
    ),
    url(
        r'^api/fe/load-variant/$',
        LoadVariantSelect.as_view(), name='load-variant'
    ),
    url(
        r'^api/fe/products-by-category/$',
        LoadProductsByCategory.as_view(), name='products-by-category'
    ),
    url(
        r'^api/fe/shipping-methods/$',
        ShippingMethodsView.as_view(), name='shipping-method'
    ),
    url(
        r'^api/fe/billing-methods/$',
        BillingMethodsView.as_view(), name='billing-method'
    ),
    url(r'^api/fe/send-unclone/$', unclone_customers),
    url(r'^api/fe/send-email/$', send_queued_mail),

    ############################
    # ===--- FRONTEND   ---=== #
    ############################
    url(
        r'^commande/media/(?!uploads)/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'media')}
    ),
    url(
        r'^commande/icons/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}
    ),
    url(
        r'^commande/img/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'img')}
    ),
    url(
        r'^commande/js/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'js')}
    ),
    url(
        r'^commande/css/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'css')}
    ),
    url(
        r'^commande/fonts/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}
    ),
    # ===---
    url(
        r'media/(?!uploads)/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'media')}
    ),
    url(
        r'icons/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}
    ),
    url(
        r'img/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'img')}
    ),
    url(
        r'js/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'js')}
    ),
    url(
        r'css/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'css')}
    ),
    url(
        r'fonts/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}
    ),
    ############################
    # ===------------------=== #
    ############################

] + extended_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + i18n_patterns( # noqa

    url(r'^message-envoye/', TemplateView.as_view(
        template_name="theme/{}/pages/message-envoye.html".format(settings.THEME_SLUG) # noqa
    )),
    url(r'^search/', include("apps.dmSearch.urls")),

    ############################
    # ===--- FRONTEND   ---=== #
    ############################
    url(r'^commande/media/(?!uploads)/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.VUE_ROOT, 'media')
    }),
    url(
        r'^commande/icons/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}
    ),
    url(
        r'^commande/img/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'img')}
    ),
    url(
        r'^commande/js/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'js')}
    ),
    url(
        r'^commande/css/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'css')}
    ),
    url(
        r'^commande/fonts/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}
    ),
    # ===---
    url(
        r'media/(?!uploads)/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'media')}
    ),
    url(
        r'icons/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}
    ),
    url(
        r'img/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'img')}
    ),
    url(
        r'js/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'js')}
    ),
    url(
        r'css/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'css')}
    ),
    url(
        r'fonts/(?P<path>.*)$',
        serve,
        {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}
    ),
    # ===---
    url(r'^commande/', TemplateView.as_view(
        template_name='theme/{}/pages/app.html'.format(settings.THEME_SLUG)
    )),
    ############################
    # ===------------------=== #
    ############################

    # MUST be the last entry!
    url('sentry-debug/', trigger_error),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('cms.urls')),
)
