from django.contrib import admin
from ihp.survey.models import Survey, SurveyConfiguration


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    ordering = (u'-create_at',)
    exclude = [u'object_id', u'content_type']
    readonly_fields = [u'reason_for_data_download', u'country',
                       u'email', u'organization', u'name', u'user', u'resource_downloaded', u'create_at']


@admin.register(SurveyConfiguration)
class SurveyConfigurationAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
