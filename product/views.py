from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Units, Category


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(Product, slug='kolenval-ogromnyj-i-ochen-dorogoj')
        return render(request, "postDetail.html", {'instance': instance})
    else:
        return render(request, 'product/category/categories.html', {'instance': instance})


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


@method_decorator(login_required, name='dispatch')
class Caregorizer(TemplateView):
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
