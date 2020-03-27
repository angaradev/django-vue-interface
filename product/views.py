# -*- coding: utf-8 -*-

import sys
import locale
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Units, Category, CarModel, AngaraOld, BrandsDict
from django.db.models import Count


#For working bulk upload parts from 1c Porter,Porter2 only
def insert_from_old(request):
    qs_from = AngaraOld.objects.all()
    i = 0
    for qa in qs_from:
        try:
            brand = BrandsDict.objects.get(id=qa.brand)
        except:
            brand = None
        try:   
            new = Product.objects.create(
                name = qa.name,
                brand = brand,
                cat_number = qa.cat_number,
                car_model = CarModel.objects.get(id=qa.car_model),
                one_c_id = qa.one_c_id,
                unit = Units.objects.get(id=1)
            )
        except Exception as e:
            print(e)
            i += 1
            print(i)
    return redirect('product-main')



#For working with categories and not tested yet
def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(
            Product, slug='kolenval-ogromnyj-i-ochen-dorogoj')
        return render(request, "postDetail.html", {'instance': instance})
    else:
        return render(request, 'product/category/categories.html', {'instance': instance})


@method_decorator(login_required, name='dispatch')
class Main(ListView):
    template_name = 'product/product_list.html'
    model = Product

    def get_queryset(self):
        if self.kwargs.get('pk', None):
            qs = self.model.objects.filter(car_model=self.kwargs['pk']).annotate(model_count=Count('car_model')).order_by('name')
            car_model = CarModel.objects.get(id=self.kwargs['pk'])
            self.request.session['car'] = {
                # 'car_make': '',
                'car_name': car_model.name,
                'car_model_id': self.kwargs['pk'],
                # 'car_engine': ''
            }
        elif self.request.session['car']['car_model_id']:
            qs = self.model.objects.filter(car_model=self.request.session['car']['car_model_id']).order_by('name')
        return qs

@method_decorator(login_required, name='dispatch')
class MainMain(ListView):
    template_name = 'product/product_list.html'
    model = Product

    def get_queryset(self):
        car_session = self.request.session.get('car', None)
        if self.kwargs.get('pk', None):
            
            qs = self.model.objects.filter(car_model=self.kwargs['pk']).annotate(model_count=Count('car_model')).order_by('name')
            self.request.session['car'] = {
                # 'car_make': '',
                'car_model_id': self.kwargs['pk'],
                # 'car_engine': ''
            }
            
        # elif car_session:
        #     qs = self.model.objects.filter(car_model=self.request.session['car']['car_model_id']).order_by('name')

        else:
            qs = self.model.objects.all().order_by('name')[:200]
        return qs
    

    





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


@method_decorator(login_required, name='dispatch')
class Categorizer(TemplateView):
    pass
    #     for drow in dic:
    #     plus = drow.plus.split('\n')
    #     plus = [x.strip() for x in plus]
    #     plus_and = plus_and_func(plus)
    #     minus = drow.minus.split('\n')
    #     minus = [x.strip() for x in minus]

    #     q_objects_key =Q()
    #     for pl_and in plus_and:
    #         q_objects_key.add(Q(reduce(operator.and_, (Q(keywords__icontains=x) for x in pl_and))), Q.OR)

    #     ker_qs = KernelTmp.objects.filter(
    #             Q(reduce(operator.or_, (Q(keywords__icontains=x) for x in plus)) |
    #                 Q(q_objects_key)
    #                 )).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus))).exclude(chk=True)
    #     ker_qs.update(group_id=drow.id, group_name=drow.name)
    # final_qs = KernelTmp.objects.all()
    # cat_count = final_qs.filter(~Q(group_id=0)).count()
    # not_cat_count = final_qs.filter(group_id=0).count()
    # request.session['categorized'] = True


def view_locale(request):
    loc_info = "getlocale: " + str(locale.getlocale()) + \
        "<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
        "<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
        "<br/>sys default encoding: " + str(sys.getdefaultencoding()) + \
        "<br/>sys default encoding: " + str(sys.getdefaultencoding())
    return HttpResponse(loc_info)
