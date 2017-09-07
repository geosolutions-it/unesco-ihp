from django import forms
from django.utils.safestring import mark_safe
import account.forms


class SignupForm(account.forms.SignupForm):
    accept = forms.BooleanField(
        required=True,
        label=mark_safe(
            'I agree to the IHP-WINS <a href="/terms-of-use" target="_blank">Terms of Use</a>'
        )
    )
