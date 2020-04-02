from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _

from ihp.survey.models import Survey


class SurveyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SurveyForm, self).__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            # set current user values as default
            self.fields['user'].initial = self.user.pk
            self.fields['name'].initial = self.user.username
            self.fields['organization'].initial = self.user.organization
            self.fields['email'].initial = self.user.email
            self.fields['country'].initial = self.user.country

            # hide all pre-filled forms
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['organization'].widget = forms.HiddenInput()
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['country'].widget = forms.HiddenInput()

    class Meta:
        model = Survey
        fields = [u'user', u'name', u'organization', u'email',
                  u'country', u'reason_for_data_download']
        widgets = {
            u'reason_for_data_download': Textarea(attrs={
                u'rows': 3,
                u'placeholder': _(u'Write a brief description '
                                  u'of how you plan to use the download.')
            }),
            u'user': forms.HiddenInput()
        }
