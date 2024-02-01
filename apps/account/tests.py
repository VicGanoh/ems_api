from rest_framework.test import APITestCase
import json
from account.models import CustomUser, Role
from rest_framework import status
from django.urls import reverse


class AuthenticationTestCase(APITestCase):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "other_names": "",
        "email": "john@example.com",
        "role": "SUPERVISOR",
        "password": "1234",
    }

    def test_create_user(self):
        url = reverse("signup")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        url = reverse("login")
        data = {
            "email": self.data.get("email"),
            "password": self.data.get("password"),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
