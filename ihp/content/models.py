from django.db import models


class TermsOfUse(models.Model):
    upload = models.FileField(upload_to='terms-of-use')

    def __str__(self):
        return "{} #{} {}".format(self.__class__.__name__, self.id,
                                  self.upload)
