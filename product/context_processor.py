from .models import CarModel, CarEngine


def session_processor(request):
    car_models = CarModel.objects.all()
    car_engines = CarEngine.objects.all()
    return {'car_models': car_models, 'car_engines': car_engines }
