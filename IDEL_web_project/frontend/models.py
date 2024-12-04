from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _


class Project(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=150, verbose_name=_('Name')),
        description=models.TextField(verbose_name=_('Description')),
    )
    photo = models.ImageField(upload_to='cards-img/', blank=True, null=True)
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Task(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=150, verbose_name=_('Name')),
        description=models.TextField(verbose_name=_('Description')),
    )
    photo = models.ImageField(upload_to='cards-img/', null=True, blank=True)
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Scale(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=150, verbose_name=_('Name')),
        description=models.TextField(verbose_name=_('Description')),
    )
    photo = models.ImageField(upload_to='cards-img/', null=True, blank=True)
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class InvestStudies(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=150, verbose_name=_('Name')),
        description=models.TextField(verbose_name=_('Description')),
    )
    photo = models.ImageField(upload_to='cards-img/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class FooterBanner(models.Model):
    facebook = models.URLField(max_length=200, default='', blank=True)
    x_twitter = models.URLField(max_length=200, default='', blank=True)
    instagram = models.URLField(max_length=200, default='', blank=True)
    threads = models.URLField(max_length=200, default='', blank=True)
    youtube = models.URLField(max_length=200, default='', blank=True)
    banner_img = models.ImageField(upload_to='cards-img/', blank=True, null=True)
    privacy_url = models.URLField(max_length=200, default='')
    cookies_policy = models.URLField(max_length=200, default='')
