from django.contrib import admin
from ihp.content.models import (TermsOfUse,
                                AboutUsPageContent,
                                ContactUsPageContent,
                                PartnerIcon,
                                FaqTopic,
                                FaqQuestion)


admin.site.register(TermsOfUse)
admin.site.register(AboutUsPageContent)
admin.site.register(ContactUsPageContent)
admin.site.register(PartnerIcon)
admin.site.register(FaqTopic)
admin.site.register(FaqQuestion)