from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import account.forms


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(label=_(u'First name'))

    last_name = forms.CharField(label=_(u'Last name'))

    accept = forms.BooleanField(
        required = True,
        label = _(u'I agree to the IHP-WINS Terms of use')
    )
