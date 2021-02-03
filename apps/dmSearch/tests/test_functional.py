
from bs4 import BeautifulSoup
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
        p.caption = "This is test 123 Product"
        p.save()

    def test_search_page(self):
        page = self.client.get(reverse('search_product'))
        self.assertEqual(page.status_code, status.HTTP_200_OK)

    def test_search_page_data(self):
        # Search result = 1 length
        page = self.client.get(reverse('search_product') + "?q=test")
        soup = BeautifulSoup(page.content)
        result = soup.findAll('div', {'class':'row search-product'})
        self.assertEqual(1, len(result))

        # Search result = 0 length
        page = self.client.get(reverse('search_product') + "?q=dmodules")
        soup = BeautifulSoup(page.content)
        result = soup.findAll('div', {'class':'row search-product'})
        self.assertEqual(0, len(result))

    def test_search_page_caption(self):
        # Search result = 1 length
        page = self.client.get(reverse('search_product') + "?q=123")
        soup = BeautifulSoup(page.content)
        result = soup.findAll('div', {'class':'row search-product'})
        self.assertEqual(1, len(result))
