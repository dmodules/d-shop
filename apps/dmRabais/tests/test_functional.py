
from django.test import TestCase
from datetime import datetime, timedelta

from dshop.models import Product

from dshop.utils_test import category, product


class CategoryDiscountTestProduct(TestCase):

    def setUp(self):
        self.cat = category()
        product(None, self.cat)

    def test_discounted_price(self):
        prod = Product.objects.all().first()

        prod.discounted_price = 50
        prod.start_date = datetime.today() - timedelta(days=2)
        prod.end_date = datetime.today() + timedelta(days=2)
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertEqual(prod.discounted_price, new_price)

    def test_discounted_price_expire(self):
        prod = Product.objects.all().first()

        prod.discounted_price = 50
        prod.start_date = datetime.today() - timedelta(days=2)
        prod.end_date = datetime.today() - timedelta(days=1)
        prod.save()

        prod = Product.objects.all().first()
        new_price = prod.get_price()
        self.assertNotEqual(prod.discounted_price, new_price)
