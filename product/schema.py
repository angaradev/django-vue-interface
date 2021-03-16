from product.models import CarModel, CarMake, Category
from graphene import String, ObjectType, ID, Field, Schema, List


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
# esh = Elasticsearch(["http://localhost:9200"])


class CategoryType(ObjectType):
    id = ID(required=True)
    type = String()
    name = String(required=True)
    slug = String(required=True)
    image = String(required=False)
    parent = ID(required=False)
    count = String()
    layout = String()


class CarMakeType(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    rusname = String()
    slug = String(required=True)
    country = String(required=True)
    priority = String()


class NewCarModelType(ObjectType):
    id = ID()
    model = String(required=True)
    rusname = String()
    year = List(String, required=True)
    engine = List(String, required=True)
    slug = String(required=True)
    make = Field(CarMakeType, required=True)
    country = String(required=True)
    priority = String()


class Query(ObjectType):

    vehicle = Field(NewCarModelType, slug=String())
    vehicles = List(NewCarModelType)
    makes = List(CarMakeType)
    make = Field(CarMakeType, slug=String(required=True))
    vehicles_by_make = List(NewCarModelType, slug=String(required=True))
    category_by_slug = Field(CategoryType, slug=String(required=True))
    category_all = List(CategoryType)

    def resolve_category_all(self, info):
        cats = Category.objects.all()
        lst = []

        for cat in cats:
            parent = None
            try:
                parent = cat.parent.id
            except:
                parent = None
            lst.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "parent": parent,
                    "image": cat.image,
                    "type": cat.type,
                    "layout": cat.layout,
                }
            )
        return lst

    def resolve_category_by_slug(self, info, slug):
        cat = Category.objects.get(slug=slug)
        try:
            parent = cat.parent.id
        except:
            parent = None
        return {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "parent": parent,
            "image": cat.image,
            "type": cat.type,
            "layout": cat.layout,
        }

    def resolve_category_by_slug(self, info, slug):
        category = Category.objects.get(slug=slug)
        return category

    def resolve_vehicles_by_make(self, info, slug):
        qs = CarModel.objects.filter(carmake__slug=slug)
        lst = []
        for car in qs:
            years = [car.year_from, car.year_to] if car.year_from else []
            lst.append(
                {
                    "id": car.id,
                    "model": car.name,
                    "rusname": car.rusname,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
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
                    "rusname": make.rusname,
                    "slug": make.slug,
                    "country": make.country.country,
                    "priority": make.priority,
                }
            )
        return lst

    def resolve_make(self, info, slug):
        make = CarMake.objects.get(slug=slug)
        return {
            "id": make.id,
            "name": make.name,
            "rusname": make.rusname,
            "slug": make.slug,
            "country": make.country.country,
            "priority": make.priority,
        }

    def resolve_vehicle(self, info, slug):
        car = CarModel.objects.get(slug=slug)
        years = [car.year_from, car.year_to] if car.year_from else []
        return {
            "id": car.id,
            "model": car.name,
            "rusname": car.rusname,
            "year": years,
            "engine": car.engine.all(),
            "slug": car.slug,
            "make": {
                "id": car.carmake.id,
                "name": car.carmake.name,
                "slug": car.carmake.slug,
                "country": car.carmake.country,
                "priority": car.carmake.priority,
            },
            "make_slug": car.carmake.slug,
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
                    "rusname": car.rusname,
                    "year": years,
                    "engine": car.engine.all(),
                    "slug": car.slug,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
                    "country": car.carmake.country,
                }
            )

        return lst


schema = Schema(query=Query)
