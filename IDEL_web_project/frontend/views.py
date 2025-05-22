from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from .models import Project, Task, InvestStudies, AboutUsContent
import json
import zipfile
import requests
from django.shortcuts import render


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_active=True)
        context['tasks'] = Task.objects.filter(is_active=True)
        context['investStudies'] = InvestStudies.objects.filter(is_active=True)

        recommended_items_all = {
            'projects': list(Project.objects.filter(is_active=True, is_recommended=True)),
            'tasks': list(Task.objects.filter(is_active=True, is_recommended=True)),
            'investstudies': list(InvestStudies.objects.filter(is_active=True, is_recommended=True)),
        }

        context['recommended_items_all'] = recommended_items_all

        return context


class AboutUsContentView(TemplateView):
    template_name = "about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_us_content'] = AboutUsContent.objects.filter(active=True).last()
        return context


class ContactView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskView(TemplateView):
    template_name = "task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('task_id')
        context['task_info'] = get_object_or_404(Task, pk=task_id)
        return context


class ProjectView(TemplateView):
    template_name = "project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_info'] = get_object_or_404(Project, pk=project_id)
        return context


class InvestView(TemplateView):
    template_name = "invest.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investstudies_id = self.kwargs.get('invest_id')
        context['invest_info'] = get_object_or_404(InvestStudies, pk=investstudies_id)
        return context

class GetConvertJzipView(TemplateView):
    template_name = 'charts_test.html'
    def get(self, request, **kwargs):

        #TODO:Quitar el 'hardcoding' siguiente
        jatos_api_url = "https://labidel.uib.es/jatos/api/v1/results/data?studyId="
        id_study = 38
        token = 'jap_aSVg4gkMX5rAdcjB8JiGvIL5ZxN6x7I7bfe0b'

        try:
            response = self.make_data_request(jatos_api_url, id_study, token)
            datos_mapeo_general = self.unzip_general_maping(BytesIO(response.content))
            datos_ready = self.specific_maping(datos_mapeo_general, id_study)

            return render(request, 'charts_test.html', {'datos_json': json.dumps(datos_ready), 'datos_generales':json.dumps(datos_mapeo_general)})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=400)

    def make_data_request(self,jatos_api_url, id_study,token):
        url = f"{jatos_api_url}{id_study}"
        headers = {
            'Authorization': f'Bearer {token}',
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=400)

    def unzip_general_maping(self, archivo_zip):
        """Descomprime el archivo .jzip y combina los datos JSON."""
        datos_generales = {}

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
                                    clave = f'StudyResultId_{study_result_id}'
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
                                    datos_generales[clave]= dic_datos_persona

                            except json.JSONDecodeError:
                                print("No hay una estructura JSON correcta")

        except Exception as e:
            print(f"Error al descomprimir el archivo .jzip: {str(e)}")

        #for clave in list(datos_generales.keys())[:2]:
            #print(clave, "→", datos_generales[clave])
        return datos_generales

    def specific_maping(self, datos_generales, id_study):
        mappings = {
            38: self.spec_mapping_OSAT,
            # otros estudios...
        }

        extractor_func = mappings.get(id_study)
        if not extractor_func:
            print(f"No hay extractor definido para el estudio {id_study}")
            return []

        return extractor_func(datos_generales)

    def spec_mapping_OSAT(self, datos_generales):
        variables_deseadas = ["mean_rt_go", "d_prima_principal", "acc_go"]
        variables_dependientes = ["genero","ciclos"]

        resultados = {var: [] for var in variables_deseadas + variables_dependientes}

        for study_results_Id, info in datos_generales.items():
            data = info.get("data", [])
            if not data:
                print(f"No hay 'data': en {study_results_Id}")
                continue

            ultimo_punto = data[-1]
            punto_inicio = data[0]

            # 1. Extraer las dependientes (no requieren condición)
            for var in variables_dependientes:
                valor = punto_inicio.get(var)
                if valor is not None:
                    resultados[var].append(valor)
                else:
                    print(f"Hay valor None en {var} de {study_results_Id}")

            # 2. Extraer las deseadas solo si se completó la tarea
            if ultimo_punto.get('prueba') == "no":
                for var in variables_deseadas:
                    valor = ultimo_punto.get(var)
                    if valor is not None:
                        resultados[var].append(valor)
                    else:
                        print(f"{var} es None en {study_results_Id}")
            else:
                print(f"{study_results_Id} no llegó al final de la tarea")

        return resultados

