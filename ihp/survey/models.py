from django.db import models

from geonode.singleton import SingletonModel
from datetime import timedelta


class Survey(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    reason_for_data_download = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'Survey pk=[{}]'.format(self.pk)


class SurveyConfiguration(SingletonModel):
    cookie_expiration_time = models.IntegerField('Cookie expiration time in hours', default=24)
    survey_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'SurveyConfiguration'

    def __str__(self):
        return 'SurveyConfiguration'
