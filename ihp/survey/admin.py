from django.contrib import admin

from ihp.survey.models import Survey, SurveyConfiguration

admin.site.register(Survey)
admin.site.register(SurveyConfiguration)
