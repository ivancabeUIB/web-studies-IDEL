from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Project, Task, Scale, InvestStudies, FooterBanner


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'is_active', 'is_recommended')


@admin.register(Task)
class TaskAdmin(TranslatableAdmin):
    list_display = ('name', 'is_active', 'is_recommended')


@admin.register(Scale)
class ScaleAdmin(TranslatableAdmin):
    list_display = ('name', 'is_active', 'is_recommended')


@admin.register(InvestStudies)
class InvestStudiesAdmin(TranslatableAdmin):
    list_display = ('name', 'is_active', 'is_active')


@admin.register(FooterBanner)
class FooterBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'x_twitter', 'cookies_policy', 'privacy_url')
