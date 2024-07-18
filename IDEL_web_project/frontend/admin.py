from django.contrib import admin
from .models import Project, Task, FooterBanner


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'is_recommended')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_recommended')


@admin.register(FooterBanner)
class FooterBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'x_twitter', 'cookies_policy', 'privacy_url')
