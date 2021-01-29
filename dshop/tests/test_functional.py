
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from dshop.models import Product
from dshop.tests.utils import filter_p, category, product

class AProductCartTest(TestCase):

    def setUp(self):
        cat = category()
        filt = filter_p()
        product(filt, cat)
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

    def test_add_to_cart(self):
        '''
            Check add to cart product
            Check max add product
        '''

        response = self.client.get(reverse("product-list") + "?format=json")
        data = response.data['results']
        product = data[0]['product_url']

        cart_data = self.client.get('http://localhost:8000/fr'+product+'/add-to-cart/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('http://localhost:8000/shop/api/cart/', cart_data.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product = data[0]['product_url']
        cart_data = self.client.get('http://localhost:8000/fr'+product+'/add-to-cart')

        cart_data = cart_data.data
        max_items = cart_data['availability']['quantity']

        cart_data['quantity'] = max_items + 10

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('http://localhost:8000/shop/api/cart/', cart_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, max_items)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DShopAPITest(TestCase):

    def setUp(self):
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
