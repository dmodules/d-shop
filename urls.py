import os
import aldryn_addons.urls

from django.conf import settings
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse
from django.contrib.sitemaps.views import sitemap
from cms.sitemaps import CMSSitemap
from dshop.sitemap import ProductSitemap

from shop.views.catalog import ProductListView

from dshop.views import CustomerView, CustomerCheckView
from dshop.views import LoadProduits, LoadProductsByCategory
from dshop.views import LoadVariantSelect
from dshop.views import ShippingMethodsView, BillingMethodsView
from dshop.views import TestPaymentView, AttributeAutocomplete
from dshop.views import PasswordResetConfirmView
from dshop.views import unclone_customers, send_queued_mail

def trigger_error(request):
    division_by_zero = 1 / 0

sitemaps = {"cmspages": CMSSitemap, "products": ProductSitemap}

def render_robots(request):
    permission = "noindex" in settings.ROBOTS_META_TAGS and "Disallow" or "Allow"
    return HttpResponse("User-Agent: *\n%s: /\n" % permission, content_type="text/plain")

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

    url(r'^attribute-autocomplete/$', AttributeAutocomplete.as_view(), name='attribute-autocomplete'),
    url(r'^robots\.txt$', render_robots),
    url(r'^sitemap\.xml$', sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    url(r'^shop/', include("shop.urls")),
    url(r'^shop/auth/password/reset-confirm/', PasswordResetConfirmView.as_view()),
    url(r'^billing-stripe/', include("apps.dmBillingStripe.urls")),
    url(r'^billing-square/', include("apps.dmBillingSquare.urls")),
    url(r'^dm-square/', include("apps.dmSquare.urls")),
    url(r'^contact/', include("apps.dmContact.urls")),
    url(r'^discount/', include("apps.dmRabais.urls")),

    url(r'^api/v1/products-list/$', ProductListView.as_view(), name='product-list'),

    url(r'^api/fe/customer/$', CustomerView.as_view(), name='customer'),
    url(r'^api/fe/customer-check/$', CustomerCheckView.as_view(), name="customer-check"),
    url(r'^api/fe/moreproduits/$', LoadProduits.as_view(), name='moreproducts'),
    url(r'^api/fe/load-variant/$', LoadVariantSelect.as_view(), name='load-variant'),
    url(r'^api/fe/products-by-category/$', LoadProductsByCategory.as_view(), name='products-by-category'),
    url(r'^api/fe/shipping-methods/$', ShippingMethodsView.as_view(), name='shipping-method'),
    url(r'^api/fe/billing-methods/$', BillingMethodsView.as_view(), name='billing-method'),
    url(r'^api/fe/send-unclone/$', unclone_customers),
    url(r'^api/fe/send-email/$', send_queued_mail),

    url(r'^test-payment/$', TestPaymentView),

] + extended_urls + aldryn_addons.urls.patterns() + i18n_patterns(

    url(r'^admin', admin.site.urls),

    url(r'^message-envoye/', TemplateView.as_view(
        template_name="theme/{}/pages/message-envoye.html".format(settings.THEME_SLUG)
    )),

    url(r'^produits/b(?P<brand_id>[0-9]+)-(?P<brand_slug>.+)$', TemplateView.as_view(
        template_name='theme/{}/pages/produits.html'.format(settings.THEME_SLUG)
    )),
    url(r'^produits/(?P<category_id>[0-9]+)-(?P<category_slug>.+)$', TemplateView.as_view(
        template_name='theme/{}/pages/produits.html'.format(settings.THEME_SLUG)
    )),
    url(r'^produits/', TemplateView.as_view(
        template_name='theme/{}/pages/produits.html'.format(settings.THEME_SLUG)
    ), name='produits'),

    url(r'^search/', include("apps.dmSearch.urls")),

    ############################
    # ===--- FRONTEND   ---=== #
    ############################
    url(r'^commande/media/(?!uploads)/(?P<path>.*)$', serve, {
        'document_root': os.path.join(settings.VUE_ROOT, 'media')
    }),
    url(r'^commande/icons/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}),
    url(r'^commande/img/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'img')}),
    url(r'^commande/js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'js')}),
    url(r'^commande/css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'css')}),
    url(r'^commande/fonts/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}),
    # ===---
    url(r'media/(?!uploads)/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'media')}),
    url(r'icons/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'icons')}),
    url(r'img/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'img')}),
    url(r'js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'js')}),
    url(r'css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'css')}),
    url(r'fonts/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.VUE_ROOT, 'fonts')}),
    # ===---
    url(r'^commande/', TemplateView.as_view(
        template_name='theme/{}/pages/app.html'.format(settings.THEME_SLUG)
    )),
    ############################
    # ===------------------=== #
    ############################

    # MUST be the last entry!
    url('sentry-debug/', trigger_error),
    *aldryn_addons.urls.i18n_patterns()
)
