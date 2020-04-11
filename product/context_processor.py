from .models import CarModel, CarEngine, CarMake, Product, Category
from django.db.models import Count


def session_processor(request):
    car_makes = CarMake.objects.all().annotate(model_count=Count('car_model'))
    #car_models = CarModel.objects.all().annotate(
    #    product_count=Count('model_product'))
    car_engines = CarEngine.objects.all()

    car_categories = Category.objects.filter(level=2)

    return {
        # 'car_models': car_models,
        'car_engines': car_engines,
        'car_makes': car_makes,
        'car_categories': car_categories
    }
