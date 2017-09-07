from django.shortcuts import redirect
from django.http.response import HttpResponseNotFound
from .models import TermsOfUse
from .forms import SignupForm
import account.views


class SignupView(account.views.SignupView):
   form_class = SignupForm


def terms_of_use_view(request):
    try:
        terms_of_use = TermsOfUse.objects.order_by('-id').get()
    except TermsOfUse.DoesNotExist:
        return HttpResponseNotFound()

    return redirect(terms_of_use.upload.url)
