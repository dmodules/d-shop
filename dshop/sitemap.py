from django.contrib.sitemaps import Sitemap
from django.conf import settings
from dshop.models import Product


class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    i18n = settings.USE_I18N

    def items(self):
        return Product.objects.filter(active=True)
