from django.views.generic.base import TemplateView
from .models import CodesForScales


class CodeForScaleView(TemplateView):
    template_name = "enter_code.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
