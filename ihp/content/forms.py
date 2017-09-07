from django import forms
from django.forms.extras.widgets import SelectDateWidget
import account.forms


class SignupForm(account.forms.SignupForm):
    accept = forms.BooleanField(required=True, label='I Accept Terms and Conditions')
