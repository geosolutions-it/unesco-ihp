from django.contrib import admin
from ihp.survey.models import Survey, SurveyConfiguration

admin.site.register(Survey)

@admin.register(SurveyConfiguration)
class SurveyConfiguration(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
