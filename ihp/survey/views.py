from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ihp.survey.forms import SurveyForm
from ihp.survey.models import SurveyConfiguration


class SurveyView(View):
    template_name = u'survey/survey.html'
    form_class = SurveyForm
    survey_configurations = SurveyConfiguration.objects.all().first()

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        download_url = request.GET.get(u'download_url', None)
        next_route = request.GET.get(u'next', None)

        # set survey_enabled to a default of True if no admin survey configuration exists
        survey_enabled = self.survey_configurations.survey_enabled if self.survey_configurations else True
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

            # set survey cookie expiration time to a default on one day if no admin survey configuration exists
            cookie_max_age = self.survey_configurations.cookie_expiration_time.total_seconds() \
                if self.survey_configurations else 86400

            response.set_cookie(
                u'ihp_dlsurvey', u'ihp_dlsurvey', max_age=cookie_max_age)
            return response

        return render(request, self.template_name, {
            u'form': form,
            u'download_url': download_url,
            u'next_route': next_route,
        })
