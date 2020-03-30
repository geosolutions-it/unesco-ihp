"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ihp.people.models import IHPProfile


@pytest.mark.django_db
class TestUserRegistration(TestCase):
    def setUp(self):
        """
        Setup tests to for user registration
        """
        self.signup_route = reverse('account_signup')

        self.registration_form_data = {
            'first_name': 'Liz',
            'last_name': 'Blair',
            'email': 'liz@blair.com',
            'password1': 'very-secret',
            'password2': 'very-secret',
            'recommendation': 'john witchel',
            'organization': 'kanzu code',
            'position': 'sample position',
            'country': 'cape verde',
            'terms_agreement': 'on',
            'request_to_join_group': [1, 2, 3]
        }

    def test_successfully_user_registration(self):
        """
        Test that a user is successfully registered on submission of valid form data
        """
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 302)

    def test_failed_user_registration_with_invalid_email(self):
        """
        Test that registration fails when an invalid email provided
        """
        self.registration_form_data['email'] = 'invalid-email-address'
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['email'], [
                         'Enter a valid email address.'])

    def test_failed_user_registration_with_different_passwords(self):
        """
        Test that registration fails when an password confirmation
        is different from the typed password
        """
        self.registration_form_data['password2'] = 'different-password'
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['password2'],
                         ['You must type the same password each time.'])

    def test_failed_user_registration_with_missing_password(self):
        """
        Test that registration fails when no passwords are provided
        """
        self.registration_form_data.pop('password1')
        self.registration_form_data.pop('password2')
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['password2'], [
                         'This field is required.'])
        self.assertEqual(response.context['form'].errors['password1'], [
                         'This field is required.'])

    def test_failed_user_registration_with_missing_names(self):
        """
        Test that registration fails when no firstname and/or last name are provided.
        NOTE: These two (i.e first and last name make up the username)
        """
        self.registration_form_data.pop('first_name')
        self.registration_form_data.pop('last_name')
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['first_name'], [
                         'This field is required.'])
        self.assertEqual(response.context['form'].errors['last_name'], [
                         'This field is required.'])

    def test_failed_user_registration_with_missing_email(self):
        """
        Test that registration fails when no email is provided
        """
        self.registration_form_data.pop('email')
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['email'], [
                         'This field is required.'])

    def test_failed_user_registration_disagreement_to_terms_of_use(self):
        """
        Test that registration fails when a user does not agree to IHP the terms of use
        """  
        self.registration_form_data.pop('terms_agreement')
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['terms_agreement'], [
                         'This field is required.'])

    def test_failed_user_registration_already_existent_email_address(self):
        """
        Test that registration fails when an email that is already in use is provided
        """
        IHPProfile.objects.create_user(**{
            "email": "liz@blair.com",
            "username": "liz-blair"
        })
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors['email'], [
                         'A user is already registered with this e-mail address.'])

    def test_failed_user_registration_with_short_names(self):
        """
        Test that registration fails when first name and/or last name are too short (i.e less than 2 characters)
        """
        self.registration_form_data['first_name'] = 'f'
        self.registration_form_data['last_name'] = 'l'
        response = self.client.post(
            self.signup_route, data=self.registration_form_data)
        self.assertEqual(response.context['form'].errors['first_name'], [
                         'Ensure this value has at least 2 characters (it has 1).'])
        self.assertEqual(response.context['form'].errors['last_name'], [
                         'Ensure this value has at least 2 characters (it has 1).'])

