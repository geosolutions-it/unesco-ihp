from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import OrderedDict

from allauth.account import forms as account_forms
from allauth.socialaccount import forms as socialaccount_forms

from allauth.account.adapter import get_adapter


class UnescoLocalAccountSignupForm(account_forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super(UnescoLocalAccountSignupForm, self).__init__(*args, **kwargs)
        _replace_username_with_first_last(self)

    def clean_recommendation(self):
        recommendation = self.cleaned_data["recommendation"]
        recommendation = get_adapter().clean_recommendation(recommendation)
        return self.cleaned_data["recommendation"]


class UnescoSocialAccountSignupForm(socialaccount_forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super(UnescoSocialAccountSignupForm, self).__init__(*args, **kwargs)
        _replace_username_with_first_last(self)


def _replace_username_with_first_last(form):
    form.fields.pop("username")
    fields = OrderedDict()
    fields["first_name"] = forms.CharField(min_length=2, label=_(u"First name"))
    fields["last_name"] = forms.CharField(min_length=2, label=_(u"Last name"))
    for key, value in form.fields.iteritems():
        fields[key] = value
    fields["recommendation"] = forms.CharField(
        min_length=2,
        max_length=50,
        required=False,
        label=_(u"Who recommended you IHP-WINS?"),
        widget=forms.TextInput(attrs={'placeholder': _("Name of the person")}))
    terms_url = "%s/terms-of-use" % settings.SITEURL
    agreement_message = _(
        "I have read and agree with the "
        "<a href={!r} target='_blank' rel='noopener noreferrer'>"
        "IHP-WINS Terms of use"
        "<a>".format(terms_url)
    )
    fields["terms_agreement"] = forms.BooleanField(label=agreement_message)
    form.fields = fields
