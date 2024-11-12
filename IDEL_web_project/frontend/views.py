from io import BytesIO
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from .models import Project, Task, Scale, FooterBanner, InvestStudies
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

        jatos_api_url = "https://labidel.uib.es/jatos/api/v1/results/data?studyId="
        get_id = 28
        url = f"{jatos_api_url}{get_id}"
        token = 'jap_7Z2FmsGbK1AJQMOvuxOiSAMikCZeRG39d50ef'

        headers = {
            'Authorization': f'Bearer {token}',
        }

        try:

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            archivo_jzip = BytesIO(response.content)
            datos_mapeados = self.descomprimir_zip_y_mapeo_general(archivo_jzip)

            return render(request, 'charts_test.html', {'datos_json': json.dumps(datos_mapeados)})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=400)

    def descomprimir_zip_y_mapeo_general(self, archivo_zip):
        """Descomprime el archivo .jzip y combina los datos JSON."""
        datos_generales = []

        try:
            with zipfile.ZipFile(archivo_zip, 'r') as archivo_zip:

                for nombre_archivo in archivo_zip.namelist():

                    if nombre_archivo.endswith('.txt'):
                        with archivo_zip.open(nombre_archivo) as archivo_txt:
                            contenido = archivo_txt.read().decode('utf-8')

                            try:
                                datos = json.loads(contenido)
                                if 'data' in datos and 'context' in datos:
                                    study_result_id = datos['context'].get('jatosStudyResultId')
                                    dic_persona_respondiendo = {f'StudyResultId_{study_result_id}':{}}
                                    dic_datos_persona = {'data':[], 'context':{}}
                                    for item,value in datos['context'].items():
                                        dic_datos_persona['context'][item] = value
                                    for respuesta in datos['data']:
                                        if 'mail' in respuesta:
                                            dic_datos_persona['context']['mail'] = respuesta['mail']
                                        else:
                                            dic_datos_persona['data'].append(respuesta)
                                    if not 'mail' in dic_datos_persona['context']:
                                        dic_datos_persona['context']['mail'] = ""
                                    dic_persona_respondiendo[f'StudyResultId_{study_result_id}']= dic_datos_persona
                                    datos_generales.append(dic_persona_respondiendo)

                            except json.JSONDecodeError:
                                print("No hay una estructura JSON correcta")

        except Exception as e:
            print(f"Error al descomprimir el archivo .jzip: {str(e)}")

        print(f'datos finales: {datos_generales}')
        return datos_generales

class TestStatisticsView(TemplateView):
    template_name = 'statistic.html'