import json

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from ...models import (
    User,
)


class BaseTestCase(APITestCase):

    def setUp(self):
        self.url = reverse_lazy("customer-list")
        self.good_user_data = {
            "first_name": "string",
            "last_name": "string",
            "email": "diogosimao@gmail.com",
            "contact_phone_number": 0,
            "mobile_phone_number": 0
        }
        user = User.objects.create(**self.good_user_data)
        user.set_password("lembrar")
        user.save()
        self.assertTrue(self.client.login(username=user.email, password="lembrar"))
        self.url = reverse_lazy("product-list")
        self.good_data = {
            "is_active": True,
            "slug": "string",
            "name": "string",
            "description": "string"
        }
        self.bad_url = "/core/api/v1/production/{pk}/".format(pk=909)
        self.bad_data = {"bad_data": 69, "slug": "", "description": "Teste"}

    def test_create_product(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], self.good_data["name"])
        self.assertEqual(response.data["slug"], self.good_data["slug"])
        self.assertEqual(response.data["description"], self.good_data["description"])
        self.good_url = reverse_lazy("product-detail", kwargs={"pk": response.data["id"]})

    def test_create_product_error(self):
        response = self.client.post(self.url, self.bad_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_list_product(self):
        response = self.client.post(self.url, self.good_data, format="json")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_product(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("product-detail", kwargs={"pk": response.data["id"]})
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], self.good_data["description"])

    def test_retrieve_product_error(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("product-detail", kwargs={"pk": response.data["id"]})
        self.good_data["description"] = "Updated"
        response = self.client.put(self.good_url, self.good_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], self.good_data["description"])

    def test_update_product_error(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("product-detail", kwargs={"pk": response.data["id"]})
        response = self.client.put(self.bad_url, self.good_data, format="json")
        self.assertEqual(response.status_code, 404)
        response = self.client.put(self.good_url, self.bad_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete_product(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("product-detail", kwargs={"pk": response.data["id"]})
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 204)

    def test_delete_product_error(self):
        response = self.client.delete(self.bad_url)
        self.assertEqual(response.status_code, 404)


class GeneratorsTestCase(TestCase):

    def test_invalid_format(self):
        try:
            args = ["api"]
            opts = {"format": "wifi", "force": True}
            call_command("generate", *args, **opts)
        except Exception as e:
            self.assertTrue(isinstance(e, CommandError))
