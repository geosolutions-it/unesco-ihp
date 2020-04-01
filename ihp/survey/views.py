from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ihp.survey.forms import SurveyForm
from ihp.survey.models import SurveyConfiguration


class SurveyView(View):
    template_name = u'survey/survey.html'
    form_class = SurveyForm
    survey_configurations = SurveyConfiguration.objects.get(pk=1)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        download_url = request.GET.get(u'download_url', u'')
        next_route = request.GET.get(u'next', u'')
        survey_enabled = self.survey_configurations.survey_enabled
        survey_cookies = request.COOKIES.get(u'survey', None)

        if not survey_enabled or (survey_enabled and survey_cookies == ""):
            return HttpResponseRedirect(download_url)

        return render(request, self.template_name, {
            u'download_url': download_url,
            u'next_route': next_route,
            u'form': form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        download_url = request.GET.get(u'download_url', u'')
        next_route = request.GET.get(u'next', u'')

        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(download_url)
            response.set_cookie(
                u'survey', max_age=self.survey_configurations.cookie_expiration_time.total_seconds())
            return response

        return render(request, self.template_name, {
            u'form': form,
            u'download_url': download_url,
            u'next_route': next_route,
        })
