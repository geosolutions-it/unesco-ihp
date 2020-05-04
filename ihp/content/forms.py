from allauth.account import forms as account_forms
from allauth.account.adapter import get_adapter
from allauth.socialaccount import forms as socialaccount_forms
from dal_select2_taggit.widgets import TaggitSelect2
from django import forms
from django.conf import settings
from django.utils.datastructures import OrderedDict
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField

from geonode.groups.models import GroupProfile
from geonode.base.enumerations import COUNTRIES
from django.db.models import Q


class UnescoLocalAccountSignupForm(account_forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super(UnescoLocalAccountSignupForm, self).__init__(*args, **kwargs)
        _replace_username_with_first_last(self)

    def clean_recommendation(self):
        recommendation = self.cleaned_data["recommendation"]
        recommendation = get_adapter().clean_recommendation(recommendation)
        return self.cleaned_data["recommendation"]

    def clean_request_to_join_group(self):
        request_to_join_group = self.cleaned_data["request_to_join_group"]
        self.fields["request_to_join_group"].initial = ['hahah']

        groups = GroupProfile.objects.filter(
            Q(access=GroupProfile.GROUP_CHOICES[0][0]) | Q(access=GroupProfile.GROUP_CHOICES[1][0]),
            pk__in=[
                # sanitize user input before saving
                request for request in request_to_join_group if request.isdigit()
            ])

        request_to_join_group = get_adapter().clean_request_to_join_group(request_to_join_group)
        self.cleaned_data["request_to_join_group"] = groups
        return self.cleaned_data["request_to_join_group"]


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
    fields["country"] = forms.ChoiceField(label=_(u"Country"), choices=COUNTRIES, required=False)

    fields["request_to_join_group"] = TagField(
        required=False,
        label=_(u"Group(s) you want to join"),
        widget=TaggitSelect2)

    terms_url = "%s/terms-of-use" % settings.SITEURL
    terms_href = "<a href={!r} target='_blank' rel='noopener noreferrer'>".format(terms_url)
    terms_href = "%s%s%s" % (terms_href, _("IHP-WINS Terms of use"), "<a>")
    agreement_message = "%s %s" % (_("I have read and agree with the "), terms_href)
    fields["terms_agreement"] = forms.BooleanField(label=agreement_message)
    form.fields = fields
