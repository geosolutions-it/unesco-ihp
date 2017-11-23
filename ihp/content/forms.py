from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import OrderedDict

from allauth.account import forms as account_forms
from allauth.socialaccount import forms as socialaccount_forms


class UnescoLocalAccountSignupForm(account_forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super(UnescoLocalAccountSignupForm, self).__init__(*args, **kwargs)
        _replace_username_with_first_last(self)


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
    terms_url = "http://ihp-wins-dev.geo-solutions.it/terms-of-use"
    agreement_message = _(
        "I have read and agree with the "
        "<a href={!r} target='_blank' rel='noopener noreferrer'>"
        "IHP-WINS Terms of use"
        "<a>".format(terms_url)
    )
    fields["terms_agreement"] = forms.BooleanField(label=agreement_message)
    form.fields = fields
