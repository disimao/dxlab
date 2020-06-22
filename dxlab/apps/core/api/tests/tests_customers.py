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
        self.good_data = {
            "user": {
                "first_name": "string",
                "last_name": "string",
                "email": "user@example.com",
                "contact_phone_number": 0,
                "mobile_phone_number": 0
            },
            "billing_information": {
                "billing_address": {
                  "street_name": "string",
                  "number": 0,
                  "additional_information": "string",
                  "postal_code": 0,
                  "state": "string",
                  "city": "string",
                  "country": "string"
                },
                "business_name": "string",
                "identification_number": "string"
            },
            "shipping_address": [
                {
                  "street_name": "string",
                  "number": 0,
                  "additional_information": "string",
                  "postal_code": 0,
                  "state": "string",
                  "city": "string",
                  "country": "string"
                }
            ]
        }
        self.good_url = ""
        self.bad_url = "/core/api/v1/production/{pk}/".format(pk=909)
        self.bad_data = {"id": 0,
                         "billing_information":
                             {"billing_address":
                                  {
                                      "identification_number": "a",
                                   }
                              }, "shipping_address": ["q"]
                         }

    def test_create_customer(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("customer-detail", kwargs={"pk": response.data["id"]})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"]["email"], self.good_data["user"]["email"])
        self.assertEqual(response.data["shipping_address"][0]["number"], 0)

    def test_create_customer_error(self):
        response = self.client.post(self.url, self.bad_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_list_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_customer(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("customer-detail", kwargs={"pk": response.data["id"]})
        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["email"], self.good_data["user"]["email"])

    def test_retrieve_customer_error(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_update_customer(self):
        self.good_data = {
            "user": {
                "first_name": "string12",
                "last_name": "string12",
                "email": "user@example12.com",
                "contact_phone_number": 0,
                "mobile_phone_number": 0
            },
            "billing_information": {
                "billing_address": {
                  "street_name": "string12",
                  "number": 0,
                  "additional_information": "string12",
                  "postal_code": 0,
                  "state": "string",
                  "city": "string",
                  "country": "string"
                },
                "business_name": "string12",
                "identification_number": "string12"
            },
            "shipping_address": [
                {
                  "street_name": "string12",
                  "number": 0,
                  "additional_information": "string12",
                  "postal_code": 0,
                  "state": "string",
                  "city": "string",
                  "country": "string"
                }
            ]
        }
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("customer-detail", kwargs={"pk": response.data["id"]})
        self.good_data["billing_information"]["identification_number"] = 39999
        self.good_data["billing_information"]["business_name"] = "Put Name"
        self.good_data["user"]["email"] = "put@example.com"
        response = self.client.put(self.good_url, self.good_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["billing_information"]["identification_number"], '39999')

    def test_update_customer_error(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("customer-detail", kwargs={"pk": response.data["id"]})
        response = self.client.put(self.bad_url, self.good_data, format="json")
        self.assertEqual(response.status_code, 404)
        response = self.client.put(self.good_url, self.bad_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete_customer(self):
        response = self.client.post(self.url, self.good_data, format="json")
        self.good_url = reverse_lazy("customer-detail", kwargs={"pk": response.data["id"]})
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 204)

    def test_delete_customer_error(self):
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
