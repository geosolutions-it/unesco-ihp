# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

import json

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
            "login": "incorect-username",
            "password": "valid-password"
        }

        self.invalid_password_form_data = {
            "login": "test@email.com",
            "password": "incorrect-password"
        }

    def test_login_success_with_email(self):
        """
        Test for sign in success with valid email and assword
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
