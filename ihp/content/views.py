from django.shortcuts import redirect
from django.http.response import HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from .models import (TermsOfUse,
                     AboutUsPageContent,
                     ContactUsPageContent,
                     PartnerIcon,
                     FaqTopic)
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


def about_us_content_view(request):
    about_us_content = None
    try:
        about_us_content = AboutUsPageContent.objects.order_by('-id').get()
    except AboutUsPageContent.DoesNotExist:
        return HttpResponseNotFound()

    partners = PartnerIcon.objects.filter().order_by('name').all()

    context = RequestContext(request, {
        'lang': get_language(),
        'obj' : about_us_content,
        'partners' : partners
    })

    return render_to_response('about_us_content_template.html', context_instance = context)


def contact_us_content_view(request):
    contact_us_content = None
    try:
        contact_us_content = ContactUsPageContent.objects.order_by('-id').get()
    except ContactUsPageContent.DoesNotExist:
        return HttpResponseNotFound()

    context = RequestContext(request, {
        'lang': get_language(),
        'obj' : contact_us_content
    })

    return render_to_response('contact_us_content_template.html', context_instance = context)


def faq_page_view(request):
    faq_topics = None
    try:
        faq_topics = FaqTopic.objects.filter().order_by('id').all()
    except FaqTopic.DoesNotExist:
        return HttpResponseNotFound()

    context = RequestContext(request, {
        'lang': get_language(),
        'obj' : faq_topics
    })

    return render_to_response('faq_page_template.html', context_instance = context)
