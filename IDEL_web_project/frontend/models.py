from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='cards-img/')
    url_to_jatos = models.URLField(max_length=200, default='')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
