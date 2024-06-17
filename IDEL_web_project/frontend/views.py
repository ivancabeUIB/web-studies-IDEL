from django.views.generic.base import TemplateView
from .models import Project


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)

        return context


class StatisticView(TemplateView):
    template_name = "statistic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statistics'] = [
            {'title': 'Card 1', 'description': 'Description for card 1'},
            {'title': 'Card 2', 'description': 'Description for card 2'},
            {'title': 'Card 3', 'description': 'Description for card 3'},
        ]

        return context
