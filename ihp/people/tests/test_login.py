import json

import pytest
from django.test import TestCase
from django.urls import reverse

from ihp.people.models import IHPProfile


@pytest.mark.django_db
class TestUserRegistration(TestCase):
    def setUp(self):
        self.user = IHPProfile.objects.create_user(**{
            "username": "valid-username",
            "email": "test@email.com",
            "password": "valid-password",
            "is_active": True
        })

        self.login_url = reverse('account_login')

        self.valid_email_and_password = {
            "login": "test@email.com",
            "password": "valid-password"
        }

        self.valid_username_and_password = {
            "login": "valid-username",
            "password": "valid-password"
        }

        self.invalid_email = {
            "login": "incorect-email@mail.com",
            "password": "valid-password"
        }

        self.invalid_username = {
            "login": "incorect-username",
            "password": "valid-password"
        }

        self.password = {
            "login": "test@email.com",
            "password": "incorrect-password"
        }

    def test_login_success_with_email(self):
        response = self.client.post(
            self.login_url, data=self.valid_email_and_password)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_success_with_username(self):
        response = self.client.post(
            self.login_url, data=self.valid_username_and_password)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_failed_login_with_incorrect_email(self):
        response = self.client.post(
            self.login_url, data=self.invalid_email)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_incorrect_username(self):
        response = self.client.post(
            self.login_url, data=self.invalid_username)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_incorrect_password(self):
        response = self.client.post(
            self.login_url, data=self.password)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_no_login_credentials(self):
        response = self.client.post(
            self.login_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
