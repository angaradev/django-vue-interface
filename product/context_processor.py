from .models import CarModel, CarEngine, CarMake
from django.db.models import Count


def session_processor(request):
    car_makes = CarMake.objects.all().annotate(model_count=Count('carmodel'))
    car_models = CarModel.objects.all().annotate(
        product_count=Count('model_product'))
    car_engines = CarEngine.objects.all()

    return {
        'car_models': car_models,
        'car_engines': car_engines,
        'car_makes': car_makes
    }
