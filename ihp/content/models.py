from django.db import models


class TermsOfUse(models.Model):
    upload = models.FileField(upload_to='terms-of-use')

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.upload)


class AboutUsPageContent(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()
    
    content_en = models.TextField()
    content_fr = models.TextField()

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)
