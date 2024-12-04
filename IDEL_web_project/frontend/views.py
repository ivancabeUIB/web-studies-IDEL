from django.views.generic.base import TemplateView
from .models import Project, Task, Scale, FooterBanner, InvestStudies


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)
        context['tasks'] = Task.objects.filter(is_active=True)
        context['scales'] = Scale.objects.filter(is_active=True)
        context['investStudies'] = InvestStudies.objects.filter(is_active=True)
        context['get_first_banner_queryset'] = FooterBanner.objects.all().first()

        # Nueva lista combinada de todos los elementos recomendados
        recommended_items = list(Project.objects.filter(is_active=True, is_recommended=True)) + \
                            list(Task.objects.filter(is_active=True, is_recommended=True)) + \
                            list(Scale.objects.filter(is_active=True, is_recommended=True)) + \
                            list(InvestStudies.objects.filter(is_active=True, is_recommended=True))

        context['recommended_items'] = recommended_items

        return context
