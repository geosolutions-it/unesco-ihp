"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import io
import urllib.parse
from http.cookies import SimpleCookie

import pytest
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from geonode.documents.models import Document
from ihp.survey.models import Survey, SurveyConfiguration
from ihp.survey.templatetags.get_survey_route import get_survey_route


@pytest.mark.django_db
class TestSurveyView(TestCase):
    def setUp(self):
        """
        Setup tests to for user survey route forms
        """
        self.imgfile = io.BytesIO(
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        gif_file = SimpleUploadedFile(
            'test_img_file.gif',
            self.imgfile.read(),
            'image/gif')
        user = get_user_model().objects.create(username='Pogba')
        self.download_resource = Document.objects.create(
            doc_file=gif_file,
            owner=user,
            title='theimg')

        # get survey route
        self.survey_route = get_survey_route(self.download_resource)

        self.survey_config = SurveyConfiguration.load()
        self.survey_config.survey_enabled = True
        self.survey_config.cookie_expiration_time = 25
        self.survey_config.save()

        self.survey_form_data = {
            "name": "Sigmon Myers",
            "organization": "Unesco",
            "email": "messi@email.com",
            "country": "DZA",
            "reason_for_data_download": "Download for research"
        }

    def test_successful_download_with_existing_cookies(self):
        """
        Test that a user with survey cookies and has filled in form correctly can download a resource
        """
        self.client.cookies = SimpleCookie({"ihp_dlsurvey": "ihp_dlsurvey"})
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.co.uk"), "/")
        )
        self.assertEqual(response.status_code, 302)

    def test_form_rendering_with_missing_survey_cookies(self):
        """
        Test that a user with with no survey cookies view the download survey form
        """
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["form"])

    def test_survey_form_prefilled_values_for_authenticate_users(self):
        """
        Test that an authenticated user receives a form with some fields pre-filled but hidden
        """
        user = get_user_model()
        user = user.objects.create_user(username="Thiago.Silver", email="Thiago@Silver.com",
                                        country="DZA", organization="PSG", password="very-secret")

        self.client.login(username=user.username, password="very-secret")
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(
            response.context["form"].fields['name'].initial, user.username)
        self.assertEqual(
            response.context["form"].fields['email'].initial, user.email)
        self.assertEqual(
            response.context["form"].fields['country'].initial, user.country)
        self.assertEqual(
            response.context["form"].fields['organization'].initial, user.organization)

    def test_survey_hidden_form_fields_for_authenticate_users(self):
        """
        Test that an authenticated user receives a form with some fields hidden
        """
        user = get_user_model()
        user = user.objects.create_user(username="Thiago.Silver", email="Thiago@Silver.com",
                                        country="DZA", organization="PSG", password="very-secret")

        self.client.login(username=user.username, password="very-secret")
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(
            response.context["form"].fields['name'].widget.__class__, forms.HiddenInput().__class__)
        self.assertEqual(
            response.context["form"].fields['email'].widget.__class__, forms.HiddenInput().__class__)
        self.assertEqual(
            response.context["form"].fields['country'].widget.__class__, forms.HiddenInput().__class__)
        self.assertEqual(
            response.context["form"].fields['organization'].widget.__class__, forms.HiddenInput().__class__)

    def test_successfully_survey_submission(self):
        """
        Test that successfully submission of the survey form redirects
        to download and sets survey cookies that prevent survey form view till it expires
        """
        response = self.client.post(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.io"), "/"),
            data=self.survey_form_data
        )
        self.assertEqual(response.status_code, 302)

        survey = Survey.objects.get(name=self.survey_form_data["name"])
        self.assertEqual(survey.name, self.survey_form_data["name"])
        self.assertIn("ihp_dlsurvey", response.client.cookies.keys())

    def test_failed_survey_submission_with_invalid_email(self):
        """
        Test that a user cannot successfully submit a form with an invalid email
        """
        self.survey_form_data["email"] = "invald-email"
        response = self.client.post(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.org"), "/"),
            data=self.survey_form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["email"], [
                         "Enter a valid email address."])

    def test_failed_survey_submission_with_missing_fields(self):
        """
        Test that a user cannot successfully submit a form with missing required fields
        """
        response = self.client.post(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/"),
            data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["name"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["email"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["reason_for_data_download"], [
                         "This field is required."])

    def test_direct_download_when_download_survey_is_disabled(self):
        """
        Test that all downloads are direct when survey configuration 'survey_enabled' = False
        i.e. survey is disabled
        """
        self.survey_config.survey_enabled = False
        self.survey_config.save()
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(response.status_code, 302)

    def test_404_returned_for_invalid_survey_route(self):
        """
        Test that an invalid survey route returns 404 error
        """
        self.survey_config.survey_enabled = False
        self.survey_config.save()
        response = self.client.get(
            u"survey/unknown/route/{}/?download_url={}&next={}".format(
                self.download_resource.pk, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(response.status_code, 404)

    def test_404_returned_for_unknown_resource_id(self):
        """
        Test that a non existing resource returns a 404 error
        """
        self.survey_config.survey_enabled = False
        self.survey_config.save()
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route.replace(str(self.download_resource.pk), '-1'),
                    urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(response.status_code, 404)
