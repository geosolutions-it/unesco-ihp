"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

import pytest
from django.test import TestCase
from django.urls import reverse

from ihp.people.models import IHPProfile


@pytest.mark.django_db
class TestUserLogin(TestCase):
    def setUp(self):
        """
        Setup tests to for user login/sign in
        """

        # create a user account
        self.user = IHPProfile.objects.create_user(**{
            "username": "valid-username",
            "email": "test@email.com",
            "password": "valid-password",
            "is_active": True
        })

        # get user login route
        self.login_url = reverse('account_login')

        self.valid_email_and_password_form_data = {
            "login": "test@email.com",
            "password": "valid-password"
        }

        self.valid_username_and_password_form_data = {
            "login": "valid-username",
            "password": "valid-password"
        }

        self.invalid_email_form_data = {
            "login": "incorect-email@mail.com",
            "password": "valid-password"
        }

        self.invalid_username_form_data = {
            "login": "incorrect-username",
            "password": "valid-password"
        }

        self.invalid_password_form_data = {
            "login": "test@email.com",
            "password": "incorrect-password"
        }

    def test_login_success_with_email(self):
        """
        Test for sign in success with valid email and password
        """
        response = self.client.post(
            self.login_url, data=self.valid_email_and_password_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_success_with_username(self):
        """
        Test for sign in success with valid username and password
        """
        response = self.client.post(
            self.login_url, data=self.valid_username_and_password_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_failed_login_with_invalid_email(self):
        """
        Test sign in failure with invalid email
        """
        response = self.client.post(
            self.login_url, data=self.invalid_email_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_invalid_username(self):
        """
        Test sign in failure with invalid username
        """
        response = self.client.post(
            self.login_url, data=self.invalid_username_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_invalid_password(self):
        """
        Test sign in failure with invalid password
        """
        response = self.client.post(
            self.login_url, data=self.invalid_password_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_failed_login_with_no_login_credentials(self):
        """
        Test sign in failure with no login credentials
        """
        response = self.client.post(
            self.login_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
