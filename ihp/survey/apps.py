from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SurveyConfig(AppConfig):
    name = 'ihp.survey'
    label = 'ihp_survey'

    def ready(self):
        super(SurveyConfig, self).ready()
        post_migrate.connect(
            self.create_default_survey_configuration, sender=self)

    def create_default_survey_configuration(self, *args, **kwargs):
        SurveyConfiguration = self.get_model('SurveyConfiguration')
        SurveyConfiguration.load()
