from django.db import models
from django import forms


class CodesForScales(models.Model):
    name = models.CharField(max_length=120)
    code_for_scale = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}. Active: {}'.format(self.name, self.is_active)
