from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ihp.survey.forms import SurveyForm
from ihp.survey.models import SurveyConfiguration


class SurveyView(View):
    template_name = u'survey/survey.html'
    form_class = SurveyForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(**{u'user': request.user})
        download_url = request.GET.get(u'download_url', None)
        next_route = request.GET.get(u'next', None)

        survey_enabled = SurveyConfiguration.load().survey_enabled
        survey_cookies = request.COOKIES.get(u'ihp_dlsurvey', None)

        if not survey_enabled or (survey_enabled and survey_cookies):
            return HttpResponseRedirect(download_url)

        return render(request, self.template_name, {
            u'download_url': download_url,
            u'next_route': next_route,
            u'form': form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        download_url = request.GET.get(u'download_url', None)
        next_route = request.GET.get(u'next', None)

        if form.is_valid() and download_url and next_route:
            form.save()
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
