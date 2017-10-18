from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class TermsOfUse(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()

    content_en = models.TextField()
    content_fr = models.TextField()

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)


class AboutUsPageContent(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()

    content_en = models.TextField()
    content_fr = models.TextField()

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)

class PartnerIcon(models.Model):
    upload = models.FileField(upload_to='partner-ico')
    name = models.CharField(max_length=255, null=False)
    href = models.TextField()

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def __init__(self, *args, **kwargs):
        super(PartnerIcon, self).__init__(*args, **kwargs)
        self._height = 164
        self._width = 164

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.name)


class ContactUsPageContent(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()

    content_en = models.TextField()
    content_fr = models.TextField()

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)


class FaqTopic(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()
    order = models.PositiveIntegerField()

    questions = models.ManyToManyField('FaqQuestion', blank=True)

    @property
    def faqs(self):
        return self.questions.filter().all()

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)


class FaqQuestion(models.Model):
    title_en = models.TextField()
    title_fr = models.TextField()

    content_en = models.TextField()
    content_fr = models.TextField()

    topic = models.ForeignKey(FaqTopic, on_delete=models.CASCADE)

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.title_en)


class DocumentationPage(MPTTModel):
    name = models.CharField(max_length=255, null=False)

    title_en = models.TextField()
    title_fr = models.TextField()
    order = models.PositiveIntegerField()

    content_en = models.TextField()
    content_fr = models.TextField()

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ("order",)
        verbose_name_plural = 'Documentation'

    class MPTTMeta:
        order_insertion_by = ['order']

    def __str__(self):
        return "{} #{} '{}'".format(self.__class__.__name__, self.id,
                                  self.name)
