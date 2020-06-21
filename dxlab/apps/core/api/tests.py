from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from rest_framework.reverse import reverse_lazy

from rest_framework.test import APITestCase

from ..models import *


class BaseTestCase(APITestCase):

    def setUp(self):
        self.url = '/api/post/'
        self.good_data = {"name": "Plano Trimestral", "slug": "plano-trimestral", "description": "Plano Classe I"}
        product = Product.objects.create(**self.good_data)
        self.good_url = reverse_lazy("product-detail", kwargs={'pk': product.id})
        self.bad_url = reverse_lazy("product-detail",  kwargs={'pk': 0})
        self.bad_data = {"bad_data": 69, "slug": "", "description": "Teste"}

    def test_create_product(self):
        response = self.client.post(self.url, self.good_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.good_data["name"])
        self.assertEqual(response.data["slug"], self.good_data["slug"])
        self.assertEqual(response.data["description"], self.good_data["description"])

    def test_create_product_error(self):
        response = self.client.post(self.url, self.bad_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_list_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_product(self):
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Plano Classe I")

    def test_retrieve_product_error(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        response = self.client.put(self.good_url, self.good_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], self.good_data["description"])

    def test_update_product_error(self):
        response = self.client.put(self.bad_url, self.good_data, format='json')
        self.assertEqual(response.status_code, 404)
        response = self.client.put(self.good_url, self.bad_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_product(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 204)

    def test_delete_product_error(self):
        response = self.client.delete(self.bad_url)
        self.assertEqual(response.status_code, 404)


class GeneratorsTestCase(TestCase):

    def test_invalid_format(self):
        try:
            args = ['api']
            opts = {'format': 'asdf', 'force': True}
            call_command('generate', *args, **opts)
        except Exception as e:
            self.assertTrue(isinstance(e, CommandError))