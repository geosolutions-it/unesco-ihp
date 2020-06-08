from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

register = template.Library()


@register.filter(name='get_survey_route')
def get_survey_route(value):
    app_label = ContentType.objects.get_for_model(value).app_label
    model = ContentType.objects.get_for_model(value).model
    return reverse('survey', args=[app_label, model, value.pk])
