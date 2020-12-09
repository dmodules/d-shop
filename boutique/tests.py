import os
from django.conf import settings
from django.core.files.images import File
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage
from django.core.mail.backends.base import BaseEmailBackend
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import override_settings

client = Client()

class SimpleTest(TestCase):

    fixtures = ['1.json', ]

    def __intt__():
        print("Data imported...")

    def test_product_list(self):
        print("Check for list of product we are getting from API")
        print("URL: http://localhost:8000/api/v1/products-list/?format=api")

        response = client.get(reverse('product-list'))
        data = response.data
        self.assertEqual(len(data), 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        print("Check add to cart API")
        
        response = client.get(reverse('product-list'))
        data = response.data['results']
        product = data[1]['product_url']
        cart_data = client.get('http://localhost:8000/fr'+product+'/add-to-cart').data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('http://localhost:8000/shop/api/cart/', cart_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        

