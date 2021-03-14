from product.models import CarModel
from graphene import String, ObjectType, ID, Field, Schema, List


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
# es = Elasticsearch(["http://localhost:9200"])


class NewCarModelType(ObjectType):
    id = ID()
    name = String()
    year = List(String)
    engine = List(String)
    slug = String()
    make = String()
    country = String()


class Query(ObjectType):

    vehicle = Field(NewCarModelType, id=String())
    vehicles = List(NewCarModelType)

    def resolve_vehicle(self, info, id):
        car = CarModel.objects.get(id=id)
        years = [car.year_from, car.year_to] if car.year_from else []
        return {
            "id": car.id,
            "name": car.name,
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
                    "name": car.name,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "make": car.carmake.name,
                    "country": car.carmake.country,
                }
            )

        return lst


schema = Schema(query=Query)
