from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='cards-img/', blank=True, null=True)
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='cards-img/')
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FooterBanner(models.Model):
    facebook = models.URLField(max_length=200, default='', blank=True)
    x_twitter = models.URLField(max_length=200, default='', blank=True)
    instagram = models.URLField(max_length=200, default='', blank=True)
    threads = models.URLField(max_length=200, default='', blank=True)
    youtube = models.URLField(max_length=200, default='', blank=True)
    banner_img = models.ImageField(upload_to='cards-img/', blank=True, null=True)
    privacy_url = models.URLField(max_length=200, default='')
    cookies_policy = models.URLField(max_length=200, default='')
