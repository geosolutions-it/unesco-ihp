from django.forms import ModelForm, Textarea

from ihp.survey.models import Survey


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = [u'name', u'organization', u'email',
                  u'country', u'reason_for_data_download']
        widgets = {
            u'reason_for_data_download': Textarea(attrs={
                u'rows': 3, u'placeholder': 'Write a brief description of how you plan to use the download.'
            }),
        }
