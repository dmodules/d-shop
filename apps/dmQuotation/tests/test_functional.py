import json
from django.contrib.auth.models import User
from django.test import TestCase
from dshop.models import Customer
from rest_framework.test import APIClient
from rest_framework import status


class QuotationFunctionalTest(TestCase):

    def setUp(self):
        user = User.objects.create(
            first_name='test',
            last_name='test',
            username='test123',
            email='test@test.test'
        )
        Customer.objects.create(user=user)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_quotation_create(self):
        response = self.client.post('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_quotation_list(self):
        response = self.client.post('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quotation_retr(self):
        response = self.client.post('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        number = json.loads(response.content)['id']
        response = self.client.get('/quotation/number/'+str(number))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quotation_number(self):
        response = self.client.post('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        number = int(json.loads(response.content)['number'])

        response = self.client.post('/quotation/list/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number + 1, int(json.loads(response.content)['number']))
        
    def test_quotation_merge(self):
        response = self.client.get('/quotation/merge-cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
