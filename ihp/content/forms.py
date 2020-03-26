from allauth.account import forms as account_forms
from allauth.account.adapter import get_adapter
from allauth.socialaccount import forms as socialaccount_forms
from django import forms
from django.conf import settings
from django.utils.datastructures import OrderedDict
from django.utils.translation import ugettext_lazy as _

from geonode.groups.models import GroupProfile


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
    for key, value in form.fields.items():
        fields[key] = value
    fields["recommendation"] = forms.CharField(
        min_length=2,
        max_length=50,
        required=False,
        label=_(u"Who recommended you IHP-WINS?"),
        widget=forms.TextInput(attrs={'placeholder': _("Name of the person")}))

    fields["organization"] = forms.CharField(min_length=2, label=_(u"Organization"),
        widget=forms.TextInput(attrs={'placeholder': _(u"Organization")}), required=False)
    fields["position"] = forms.CharField(min_length=2, label=_(u"Position"),
        widget=forms.TextInput(attrs={'placeholder': _(u"Position")}), required=False)
    fields["country"] = forms.CharField(min_length=2, label=_(u"Country"),
        widget=forms.TextInput(attrs={'placeholder': _(u"Country")}), required=False)

    fields["request_to_join_group"] = forms.ModelMultipleChoiceField(
        queryset=GroupProfile.objects.all(),
        required=False,
        label=_(u"Group(s) you want to join"))

    terms_url = "%s/terms-of-use" % settings.SITEURL
    terms_href = "<a href={!r} target='_blank' rel='noopener noreferrer'>".format(terms_url)
    terms_href = "%s%s%s" % (terms_href, _("IHP-WINS Terms of use"), "<a>")
    agreement_message = "%s %s" % (_("I have read and agree with the "), terms_href)
    fields["terms_agreement"] = forms.BooleanField(label=agreement_message)
    form.fields = fields
