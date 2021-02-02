
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from dshop.tests.utils import \
    category, \
    product

class CategoryDiscountTestProduct(TestCase):

    def setUp(self):
        self.client = Client()
        self.cat = category()
        p = product(None, self.cat)
        p.description = "This is test Product"
        p.save()

    def test_search_page(self):
        page = self.client.get((reverse('search_product')))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
