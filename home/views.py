from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from home.models import Documentation


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        # <view logic>
        return {}


class DocumentationView(TemplateView):
    template_name = 'home/documentation.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        some_data =  Documentation.objects.all()
        context.update({'documentation': some_data})
        return context
