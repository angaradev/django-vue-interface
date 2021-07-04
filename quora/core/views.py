from django.contrib.auth.mixins import LoginRequireMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.http import require_GET


class IndexTemplateView(TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return template_name
