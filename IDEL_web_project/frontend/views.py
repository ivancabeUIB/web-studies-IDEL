from django.views.generic.base import TemplateView
from .models import Project, Task, FooterBanner


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)
        context['recommended_projects'] = Project.objects.filter(is_active=True, is_recommended=True)
        context['get_first_banner_queryset'] = FooterBanner.objects.all()[0]

        return context
