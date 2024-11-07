from io import BytesIO
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from .models import Project, Task, Scale, FooterBanner, InvestStudies
import os
import json
import zipfile
import requests
from django.shortcuts import render
from django.views import View
from django.conf import settings

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

class ObtenerConvertirJzipGraficarView(TemplateView): #TODO:Separar responsabilidades de cada función
    template_name = 'charts_test.html'
    def get(self, request, **kwargs):
        # Definir la URL de la API de JATOS para obtener el archivo .jzip
        jatos_api_url = "https://labidel.uib.es/jatos/api/v1/results/data?studyId="
        get_id = 28
        url = f"{jatos_api_url}{get_id}"
        token = 'jap_7Z2FmsGbK1AJQMOvuxOiSAMikCZeRG39d50ef'

        headers = {
            'Authorization': f'Bearer {token}',
        }

        try:
            # Realizar la solicitud GET a la API de JATOS para obtener el archivo .jzip
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            #print(response.content) -> Checkeado: Correcto. El contenido se recibe correctamente

            # Cargar el contenido de response como un archivo ZIP en memoria
            archivo_jzip = BytesIO(response.content)
            # Descomprimir el archivo .zip
            datos_combinados = self.descomprimir_jzip(archivo_jzip)

            # Pasar los datos al template para graficar
            return render(request, 'charts_test.html', {'datos_json': json.dumps(datos_combinados)})

        except requests.exceptions.RequestException as e:
            # Si ocurre algún error durante la solicitud GET
            return JsonResponse({'error': str(e)}, status=400)

    def descomprimir_jzip(self, archivo_jzip):
        """Descomprime el archivo .jzip y combina los datos JSON."""
        datos_combinados = []

        try:
            # Abre y descomprime el archivo .jzip como un archivo ZIP
            with zipfile.ZipFile(archivo_jzip, 'r') as archivo_zip:
                print(archivo_zip)
                for nombre_archivo in archivo_zip.namelist():
                    print(nombre_archivo)
                    if nombre_archivo.endswith('.txt'):
                        # Cargar el contenido de cada archivo .txt
                        with archivo_zip.open(nombre_archivo) as archivo_txt:
                            contenido = archivo_txt.read().decode('utf-8')

                            # Intentar convertir el contenido a JSON
                            try:
                                datos = json.loads(contenido)
                                datos_combinados.append(datos)
                                print(f"El archivo {nombre_archivo} esá en formato JSON")
                            except json.JSONDecodeError:
                                print(f"El archivo {nombre_archivo} no está en formato JSON.")
                                print(f"El formato es este: {contenido}")

        except Exception as e:
            # Si hay un error durante la descompresión
            raise ValueError(f"Error al descomprimir el archivo .jzip: {str(e)}")

        return datos_combinados