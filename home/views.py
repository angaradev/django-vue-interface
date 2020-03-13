from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        # <view logic>
        return {}
