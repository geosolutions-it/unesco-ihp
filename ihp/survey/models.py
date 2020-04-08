from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from geonode.base.enumerations import COUNTRIES
from geonode.singleton import SingletonModel


class Survey(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name=u'survey_user+',
        null=True,
        blank=True)

    name = models.CharField(_(u'Name'), max_length=255)
    organization = models.CharField(
        max_length=255,
        blank=True,
        null=True)

    email = models.EmailField(_(u'Email'))

    country = models.CharField(
        _(u'Country'),
        choices=COUNTRIES,
        max_length=3,
        blank=True,
        null=True,)

    reason_for_data_download = models.TextField(_(u'Reason for data download'))

    # reference to the resource that was downloaded
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    downloaded_resource = GenericForeignKey()

    create_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_profile(self):
        """
        Return a link to the user's profile
        """
        if self.user:
            escaped_username = escape(self.user.username)
            user_profile_link = reverse(
                'profile_detail', args=[escaped_username])
            return mark_safe('<a target="_blank" href="{}">{}</a>'.format(user_profile_link, escaped_username))
        return '-'

    @property
    def user_email(self):
        """
        Return a link to the survey user's email
        """
        escaped_user_email = escape(self.email)
        return mark_safe('<a target="_blank" href="mailto:{}">{}</a>'.format(escaped_user_email, escaped_user_email))

    @property
    def resource_downloaded(self):
        """
        Return resource link as html in django admin
        """
        resource_name_mapper = {
            'document': (lambda obj: (obj.id, 'document_detail')),
            'layer':  (lambda obj: (obj.alternate, 'layer_detail'))
        }

        object_params = resource_name_mapper[str(self.content_type)]
        resource_link = reverse(object_params(self.downloaded_resource)[1], args=[
                                object_params(self.downloaded_resource)[0]])

        return mark_safe('<a target="_blank" href="{}">{}</a>'.format(
            escape(resource_link), escape(self.downloaded_resource)))

    def __str__(self):
        return u'Survey from {} ({})'.format(self.name, self.create_at.date())


class SurveyConfiguration(SingletonModel):
    cookie_expiration_time = models.IntegerField(
        u'Cookie expiration time in hours', default=24)
    survey_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = u'SurveyConfiguration'

    def __str__(self):
        return u'SurveyConfiguration'
