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
        token = 'jap_7Z2FmsGbK1AJQMOvuxOiSAMikCZeRG39d50ef' #Creado 7/11/2024. Caduca en 1 mes.

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
            datos_mapeados = self.descomprimir_jzip_y_mapeo_general(archivo_jzip)

            #Llamar función que mapee de una forma concreta para un grafico concreto

            # Pasar los datos al template para graficar
            return render(request, 'charts_test.html', {'datos_json': json.dumps(datos_mapeados)})

        except requests.exceptions.RequestException as e:
            # Si ocurre algún error durante la solicitud GET
            return JsonResponse({'error': str(e)}, status=400)

    def descomprimir_jzip_y_mapeo_general(self, archivo_jzip):
        """Descomprime el archivo .jzip y combina los datos JSON."""
        datos_generales = []
        count_JSON = 0
        count_Total = 0
        try:
            # Abre y descomprime el archivo .jzip como un archivo ZIP
            with zipfile.ZipFile(archivo_jzip, 'r') as archivo_zip:

                for nombre_archivo in archivo_zip.namelist():

                    if nombre_archivo.endswith('.txt'):
                        # Cargar el contenido de cada archivo .txt
                        with archivo_zip.open(nombre_archivo) as archivo_txt:
                            contenido = archivo_txt.read().decode('utf-8')
                            try:
                                # Intentar convertir el contenido a JSON
                                datos = json.loads(contenido)
                                if 'data' in datos and isinstance(datos['data'], list):
                                    dic_persona_respondiendo = {f"StudyResultId_{datos['context']['jatosStudyResultId']}":[]}
                                    # Iterar sobre cada elemento en 'data'
                                    for respuesta in datos['data']:
                                        if 'mail' not in respuesta:
                                            #añadir la respuesta a datos_graficables
                                            dic_persona_respondiendo[f"StudyResultId_{datos['context']['jatosStudyResultId']}"].append(respuesta)
                                    datos_generales.append(dic_persona_respondiendo)
                                count_JSON +=1
                                count_Total +=1
                            except json.JSONDecodeError:
                                count_Total +=1

        except Exception as e:
            # Si hay un error durante la descompresión
            raise ValueError(f"Error al descomprimir el archivo .jzip: {str(e)}")
        print(f"JSON:{count_JSON},Total:{count_Total}")
        print("Datos generales:", datos_generales[:2])
        return datos_generales