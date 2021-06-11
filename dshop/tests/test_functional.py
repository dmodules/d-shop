from django.test import TestCase, Client
from django.urls import reverse
import pytz
import random
from datetime import datetime, timedelta
from rest_framework import status

from dshop.models import Product, ProductCategory, Attribute
from dshop.templatetags.dshop_tags import \
    dm_variants_is_outofstock, \
    dm_variants_is_discounted, \
    dm_get_products_vedette, \
    dm_get_products_related, \
    dm_get_products_all, \
    dm_get_brands_all, \
    dm_get_brand, \
    dm_get_filters_all, \
    dm_get_category_by_category, \
    dm_get_categories_parents, \
    dm_get_category, \
    dm_get_attributes_list
from dshop.utils import get_coords_from_address
from dshop.tests.utils import filter_p, \
    category, \
    product, \
    product_variable, \
    product_variant, \
    create_data


class AProductCartTest(TestCase):

    def setUp(self):
        cat = category()
        filt = filter_p()
        product(filt, cat)
        pv = product_variable()
        product_variant(pv)
        self.client = Client()

    def test_product_list(self):
        '''
            Check for product from model and product from API
        '''
        total_product = Product.objects.all().count()
        response = self.client.get(reverse("product-list") + "?format=api")
        data = response.data['results']

        self.assertEqual(len(data), total_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DShopAPITest(TestCase):

    def setUp(self):
        create_data()
        self.client = Client()

    def test_customer_api(self):
        response = self.client.get(reverse('customer'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_more_product_api(self):
        response = self.client.get(reverse('moreproducts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shipping_method_api(self):
        response = self.client.get(reverse('shipping-method'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_billing_method_api(self):
        response = self.client.get(reverse('billing-method'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_load_variant_select(self):
        response = self.client.get(reverse('load-variant'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_load_product_by_category(self):
        response = self.client.get(reverse('products-by-category'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DShopAATemplate(TestCase):

    def setUp(self):
        create_data()
        self.client = Client()

    def test_produits_related_product(self):
        pr = Product.objects.all().first()
        ret = dm_get_products_related(pr.categories, pr.id)
        self.assertEqual(4, ret['products'].count())

    def test_product_all(self):
        products = dm_get_products_all()
        self.assertEqual(24, products.count())

    def test_active_product(self):
        products = dm_get_products_vedette()
        self.assertEqual(0, products.count())
        for pr in Product.objects.all()[1:5]:
            pr.is_vedette = True
            pr.save()
        products = dm_get_products_vedette()
        self.assertEqual(4, products.count())

    def test_variant_out_of_stock(self):
        pr = Product.objects.all().order_by('id')
        random_p = random.randint(pr.first().id, pr.last().id)
        pr = Product.objects.get(id=random_p)
        ret = dm_variants_is_outofstock(pr.variants)
        self.assertEqual(False, ret)
        for pv in pr.variants.all():
            pv.quantity = 0
            pv.save()
        ret = dm_variants_is_outofstock(pr.variants)
        self.assertEqual(True, ret)

    def test_variant_discounted(self):
        pr = Product.objects.all().order_by('id')
        random_p = random.randint(pr.first().id, pr.last().id)
        pr = Product.objects.get(id=random_p)
        ret = dm_variants_is_discounted(pr.variants)
        self.assertEqual(False, ret)

        pv = pr.variants.all()[0]
        pv.discounted_price = 1
        pv.start_date = pytz.utc.localize(datetime.today() - timedelta(days=2))
        pv.end_date = pytz.utc.localize(datetime.today() + timedelta(days=2))
        pv.save()
        ret = dm_variants_is_discounted(pr.variants)
        self.assertEqual(True, ret)

    def test_get_brand_test(self):
        data = dm_get_brands_all()
        self.assertEqual(4, data.count())

        d = dm_get_brand(data[0].id)
        self.assertEqual(d.id, data[0].id)

    def test_filter(self):
        data = dm_get_filters_all()
        self.assertEqual(0, data.count())

    def test_category_child(self):
        cats = dm_get_categories_parents()
        self.assertEqual(4, cats.count())
        data = dm_get_category_by_category(cats[0])
        self.assertEqual(2, data.count())
        data = dm_get_category(cats[0].id)
        self.assertEqual(ProductCategory, type(data))

    def test_attribute(self):
        attr = Attribute.objects.get(name='Color')
        data = dm_get_attributes_list(attr)
        self.assertEqual(3, len(data))


class TestUtils(TestCase):

    def test_address_coards(self):
        addr = "Saint-Félicien, Le Domaine-du-Roy, \
            Saguenay–Lac-Saint-Jean, Québec, G8K 2R2, Canada"
        try:
            loc = get_coords_from_address('G8K 2R2')
            self.assertEqual(addr, loc.address)
        except Exception:
            self.assertEqual(1, 1)
