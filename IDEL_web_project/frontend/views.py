from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from .models import Project, Task, FooterBanner, InvestStudies, HeaderImage, AboutUsContent


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
