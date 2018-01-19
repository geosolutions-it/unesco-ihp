from django.contrib import admin

from photologue.admin import PhotoAdmin
from photologue.models import Photo

from . import models


def photo_url(photo_instance):
    url = photo_instance.image.url
    return u'<a href="{0}">{0}</a>'.format(url)
photo_url.allow_tags = True


class CustomPhotoAdmin(PhotoAdmin):
    list_display = PhotoAdmin.list_display + (photo_url,)


admin.site.register(models.TermsOfUse)
admin.site.register(models.AboutUsPageContent)
admin.site.register(models.ContactUsPageContent)
admin.site.register(models.PartnerIcon)
admin.site.register(models.FaqTopic)
admin.site.register(models.FaqQuestion)
admin.site.register(models.DocumentationPage)

admin.site.unregister(Photo)
admin.site.register(Photo, CustomPhotoAdmin)
