from product.models import CarModel, CarMake
from graphene import String, ObjectType, ID, Field, Schema, List


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
# es = Elasticsearch(["http://localhost:9200"])


class NewCarModelType(ObjectType):
    id = ID()
    model = String()
    year = List(String)
    engine = List(String)
    slug = String()
    make = String()
    country = String()


class CarMakeType(ObjectType):
    id = ID()
    name = String()
    slug = String()
    country = String()


class Query(ObjectType):

    vehicle = Field(NewCarModelType, id=String())
    vehicles = List(NewCarModelType)
    makes = List(CarMakeType)
    vehicles_by_make = List(NewCarModelType, make=String(required=True))

    def resolve_vehicles_by_make(self, info, make):
        qs = CarModel.objects.filter(carmake__name=make)
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "make": car.carmake.name,
                    "country": car.carmake.country,
                }
            )
        return lst

    def resolve_makes(self, info):
        qs = CarMake.objects.all()
        lst = []
        for make in qs:
            lst.append(
                {
                    "id": make.id,
                    "name": make.name,
                    "slug": make.slug,
                    "country": make.country.country,
                }
            )
        return lst

    def resolve_vehicle(self, info, id):
        car = CarModel.objects.get(id=id)
        years = [car.year_from, car.year_to] if car.year_from else []
        return {
            "id": car.id,
            "model": car.name,
            "year": years,
            "engine": car.engine.all(),
            "slug": car.slug,
            "make": car.carmake.name,
            "country": car.carmake.country,
        }

    def resolve_vehicles(self, info):
        qs = CarModel.objects.all()
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "make": car.carmake.name,
                    "country": car.carmake.country,
                }
            )

        return lst


schema = Schema(query=Query)
