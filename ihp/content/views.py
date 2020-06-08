from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.utils.translation import get_language
from .models import (TermsOfUse,
                     AboutUsPageContent,
                     ContactUsPageContent,
                     PartnerIcon,
                     FaqTopic,
                     DocumentationPage)


def terms_of_use_view(request):
    terms_of_use = None
    try:
        terms_of_use = TermsOfUse.objects.order_by('-id').get()
    except TermsOfUse.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'lang': get_language(),
        'obj' : terms_of_use
    }

    return render(request, 'terms_of_use_template.html', context=context)


def about_us_content_view(request):
    about_us_content = None
    try:
        about_us_content = AboutUsPageContent.objects.order_by('-id').get()
    except AboutUsPageContent.DoesNotExist:
        return HttpResponseNotFound()

    partners = PartnerIcon.objects.filter().order_by('name').all()

    context = {
        'lang': get_language(),
        'obj' : about_us_content,
        'partners' : partners
    }

    return render(request, 'about_us_content_template.html', context=context)


def contact_us_content_view(request):
    contact_us_content = None
    try:
        contact_us_content = ContactUsPageContent.objects.order_by('-id').get()
    except ContactUsPageContent.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'lang': get_language(),
        'obj' : contact_us_content
    }

    return render(request, 'contact_us_content_template.html', context=context)


def faq_page_view(request):
    faq_topics = None
    try:
        faq_topics = FaqTopic.objects.filter().order_by('id').all()
    except FaqTopic.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'lang': get_language(),
        'obj' : faq_topics
    }

    return render(request, 'faq_page_template.html', context=context)


def documentation_page_view(request, pk=1):
    doc_pages = None
    toc = None
    max_depth = 1
    try:
        doc_root = DocumentationPage.objects.get(pk=pk)
        doc_pages = DocumentationPage.objects.get(pk=pk)\
            .get_descendants(include_self=True)\
            .filter(level__lte=doc_root.level + max_depth)\
            .order_by('order').all()
        toc = DocumentationPage.objects.filter(level__lte=1)\
            .order_by('order').all()
    except DocumentationPage.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'lang': get_language(),
        'obj' : doc_pages,
        'toc' : toc,
        'pk' : int(pk)
    }

    return render(request, 'doc_page_template.html', context=context)
