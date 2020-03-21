from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Units
@method_decorator(login_required, name='dispatch')
class Main(ListView):
    template_name = 'product/product_list.html'
    model = Product


@method_decorator(login_required, name='dispatch')
class CreateView(TemplateView):
    template_name = 'product/product_new.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class Detail(TemplateView):
    template_name = 'product/product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        units_list = Units.objects.all()
        context = {
            'object': product,
            'units_list': units_list
        }
        return render(request, self.template_name, context)
