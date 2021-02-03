
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from bs4 import BeautifulSoup

from dshop.models import Product
from dshop.utils import get_coords_from_address
from dshop.tests.utils import filter_p, \
    category, \
    product, \
    product_variable, \
    product_variant

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

    ''''def test_add_to_cart_default_product(self):
        response = self.client.get(reverse("product-list") + "?format=json")
        data = response.data['results']
        quantity = 0
        for product in data:
            product_url = product['product_url']
            if product['product_model'] == "productdefault":
                # Get cart data
                product_url = product_url[1:].split('/')[1]
                url = 'http://localhost:8000/fr/produit/'+product_url+'/add-to-cart'
                cart_data = self.client.get(url)
                quantity += cart_data.data['quantity']
                cart_url = 'http://localhost:8000/shop/api/cart/'
                response = self.client.post(cart_url, cart_data.data)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, quantity)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart_max_quantity(self):
        response = self.client.get(reverse("product-list") + "?format=json")
        data = response.data['results']
        quantity = 0
        for product in data:
            product_url = product['product_url']
            if product['product_model'] == "productdefault":
                # Get cart data
                product_url = product_url[1:].split('/')[1]
                url = 'http://localhost:8000/fr/produit/'+product_url+'/add-to-cart'
                cart_data = self.client.get(url)
                break

        cart_data = cart_data.data
        max_items = cart_data['availability']['quantity']

        cart_data['quantity'] = max_items + 10

        # Call add to cart API
        response = self.client.post('http://localhost:8000/shop/api/cart/', cart_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check cart data
        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, max_items)
        self.assertEqual(response.status_code, status.HTTP_200_OK)'''

    '''def test_add_to_cart_variable_product(self):
        response = self.client.get(reverse("product-list") + "?format=json")
        data = response.data['results']
        quantity = 0
        for product in data:
            product_url = product['product_url']
            if product['product_model'] == "productvariable":
                # Get cart data
                product_url = product_url[1:].split('/')[1]
                url = 'http://localhost:8000/fr/produit/'+product_url+'/add-productvariable-to-cart'
                cart_data = self.client.get(url)
                print(cart_data.data)
                quantity += cart_data.data['quantity']
                cart_url = 'http://localhost:8000/shop/api/cart/'
                response = self.client.post(cart_url, cart_data.data)
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, quantity)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart_variable_product_max(self):
        response = self.client.get(reverse("product-list") + "?format=json")
        data = response.data['results']
        print(data)
        quantity = 0
        for product in data:
            product_url = product['product_url']
            if product['product_model'] == "productvariable":
                # Get cart data
                product_url = product_url[1:].split('/')[1]
                url = 'http://localhost:8000/fr/produit/'+product_url+'/add-productvariable-to-cart'
                cart_data = self.client.get(url)
                print(cart_data)
                break

        cart_data = cart_data.data
        max_items = cart_data['availability']['quantity']

        cart_data['quantity'] = max_items + 10
        response = self.client.get('http://localhost:8000/shop/api/cart/')
        item_in_cart = response.data['total_quantity']

        self.assertEqual(item_in_cart, max_items)
        self.assertEqual(response.status_code, status.HTTP_200_OK)'''


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

class DShopTemplate(TestCase):

    def setUp(self):
        pv = product_variable()
        product_variant(pv)
        data = {
            'product_name': 'Lemon',
            'slug': 'lemon',
            'order': 0,
            'caption': 'Lemon'
        }
        pv = product_variable(data)
        data = {
            'product': pv,
            'product_code': '00002',
            'unit_price': 10,
            'quantity': 1,
        }
        product_variant(pv, data)
        self.client = Client()

    def test_produits_page(self):
        p_count = Product.objects.all().count()

        response = self.client.get('http://localhost:8000/fr/produits/')
        soup = BeautifulSoup(response.content, features="lxml")
        div = soup.find('div', {'class': 'row shop_container grid produits'})
        divs = div.findAll('div', {'class': 'produit col-md-4 col-6'})

        self.assertEqual(p_count, len(divs))

class TestUtils(TestCase):

    def test_address_coards(self):
        addr = "Saint-Félicien, Le Domaine-du-Roy, Saguenay–Lac-Saint-Jean, Québec, G8K 2R2, Canada"
        loc = get_coords_from_address('G8K 2R2')
        self.assertEqual(addr, loc.address)
