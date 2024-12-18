from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import CodesForScales
from .forms import CodeForm
from django.utils.translation import gettext as _


class EnterScaleCodeView(TemplateView):
    template_name = 'scale_code_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CodeForm()  # Formulario vacío al cargar la página
        return context

    def post(self, request, *args, **kwargs):
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                scale = CodesForScales.objects.get(code_for_scale=code, is_active=True)
                messages.success(request, _('¡Código válido! Accediendo a los baremos...'))
            except CodesForScales.DoesNotExist:
                messages.error(request, _('El código no es válido o está inactivo.'))
        else:
            messages.error(request, _('Por favor, revisa el formulario.'))

        return self.render_to_response({'form': form})
