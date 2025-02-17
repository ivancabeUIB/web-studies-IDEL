import json
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render
from .forms import ChatbotForm
from .projecte_anubis.chatbot import call_from_api


class ChatbotAPI(View):
    """Vista basada en clases para manejar solicitudes POST al chatbot API."""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            if not message:
                return JsonResponse({"error": "No message provided"}, status=400)

            response_text = call_from_api(message)
            return JsonResponse({"response": response_text})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def get(self, request, *args, **kwargs):
        """Devuelve un error si se intenta acceder con GET."""
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


class ChatbotTesting(TemplateView):
    """Vista para renderizar la página del chatbot y manejar el formulario."""

    template_name = "test_ai_chatbot.html"

    def get_context_data(self, **kwargs):
        """Agrega el formulario y valores adicionales al contexto."""
        context = super().get_context_data(**kwargs)
        context["form"] = ChatbotForm()
        context["response_from_api"] = kwargs.get("response_from_api")  # Se obtiene la respuesta si existe
        print("CONTEXTO", context["response_from_api"])
        return context

    def post(self, request, *args, **kwargs):
        """Maneja la solicitud POST desde el formulario."""
        form = ChatbotForm(request.POST)
        response_message = None

        if form.is_valid():
            message = form.cleaned_data["message"]
            print("Mensaje enviado:", message)
            response_message = call_from_api(message)
            print("Respuesta de la API:", response_message)

        # Renderiza la plantilla con el contexto actualizado
        return self.render_to_response(self.get_context_data(response_from_api=response_message, form=form))

