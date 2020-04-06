from django.contrib import admin
from ihp.survey.models import Survey, SurveyConfiguration


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    ordering = (u'-create_at',)
    fields = ['reason_for_data_download', 'country', 'email',
              'organization', 'name', 'user', 'resource_downloaded']
    readonly_fields = ['reason_for_data_download', 'country',
                       'email', 'organization', 'name', 'user', 'resource_downloaded']


@admin.register(SurveyConfiguration)
class SurveyConfigurationAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
