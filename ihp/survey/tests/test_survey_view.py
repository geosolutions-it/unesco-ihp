"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import urllib.parse

import pytest
from django.test import TestCase
from django.urls import reverse

from ihp.survey.models import Survey
from http.cookies import SimpleCookie


@pytest.mark.django_db
class TestSurveyView(TestCase):
    def setUp(self):
        """
        Setup tests to for user survey route forms
        """
        # get survey route
        self.survey_route = reverse("survey")

        self.survey_form_data = {
            "name": "Sigmon Myers",
            "organization": "Unesco",
            "email": "messi@email.com",
            "country": "Ecuador",
            "reason_for_data_download": "Download for research"
        }

    def test_successful_download_with_existing_cookies(self):
        self.client.cookies = SimpleCookie({"ihp_dlsurvey": "ihp_dlsurvey"})
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.co.uk"), "/")
        )
        self.assertEqual(response.status_code, 302)

    def test_form_rendering_with_missing_survey_cookies(self):
        response = self.client.get(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/")
        )
        self.assertEqual(response.status_code, 200)

    def test_successfully_survey_submission(self):
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
        response = self.client.post(
            u"{}?download_url={}&next={}".format(
                self.survey_route, urllib.parse.quote("http://example.com"), "/"),
            data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].errors["name"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["organization"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["email"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["country"], [
                         "This field is required."])
        self.assertEqual(response.context["form"].errors["reason_for_data_download"], [
                         "This field is required."])
