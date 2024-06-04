from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cards'] = [
            {'title': 'Card 1', 'description': 'Description for card 1'},
            {'title': 'Card 2', 'description': 'Description for card 2'},
            {'title': 'Card 3', 'description': 'Description for card 3'},
        ]

        return context
