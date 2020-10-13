from django.apps import apps
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from ihp.survey.forms import SurveyForm
from ihp.survey.models import SurveyConfiguration


class SurveyView(View):
    template_name = u'survey/survey.html'
    form_class = SurveyForm

    def get(self, request, *args, **kwargs):
        self.get_download_resource(**kwargs)
        form = self.form_class(**{u'user': request.user})
        download_url = request.GET.get(u'download_url', None)
        next_route = request.GET.get(u'next', None)

        survey_enabled = SurveyConfiguration.load().survey_enabled
        survey_cookies = request.COOKIES.get(u'ihp_dlsurvey', None)

        if not survey_enabled or (survey_enabled and survey_cookies) or request.user.is_superuser:
            return HttpResponseRedirect(download_url)

        return render(request, self.template_name, {
            u'download_url': download_url,
            u'next_route': next_route,
            u'form': form
        })

    def post(self, request, *args, **kwargs):
        self.get_download_resource(**kwargs)
        form = self.form_class(request.POST)
        download_url = request.GET.get(u'download_url', None)
        next_route = request.GET.get(u'next', None)

        if form.is_valid() and download_url and next_route:
            survey = form.save()
            survey.downloaded_resource = self.downloaded_resource
            survey.save()
            response = HttpResponseRedirect(download_url)

            cookie_max_age = SurveyConfiguration.load().cookie_expiration_time * 3600

            response.set_cookie(
                u'ihp_dlsurvey', u'ihp_dlsurvey', max_age=cookie_max_age)
            return response

        return render(request, self.template_name, {
            u'form': form,
            u'download_url': download_url,
            u'next_route': next_route,
        })

    def get_download_resource(self, **kwargs):
        """
        Get download resource object else return 404
        """
        app_label = kwargs.get('app_label')
        model = kwargs.get('model')
        resource_id = kwargs.get('resource_id')

        try:
            resource_model = apps.get_model('{}.{}'.format(app_label, model))
            self.downloaded_resource = get_object_or_404(
                resource_model, pk=resource_id)
        except LookupError:
            raise Http404
