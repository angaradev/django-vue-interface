from product.models import CarModel, CarMake, Category, Product
from graphene import String, ObjectType, ID, Field, Schema, List, Boolean
from django.db.models import Count
from .utils import chk_img


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
    count = String()


class IProductImagesType(ObjectType):
    id = ID()
    img150 = String(required=True)
    img245 = String(required=True)
    img500 = String(required=True)
    img800 = String(required=True)
    img245x245 = String(required=True)
    img150x150 = String(required=True)
    img500x500 = String(required=True)
    img800x800 = String(required=True)
    main = Boolean(required=True)


class PopularProductByModelType(ObjectType):
    id = ID()
    slug = String(required=True)
    name = String(required=True)
    name2 = String(required=True)
    full_name = String(required=True)
    one_c_id = String(required=True)
    sku = String(required=True)
    model = List(NewCarModelType, required=True)
    images = List(IProductImagesType)
    cat_number = String(required=True)
    bages = String(required=True)


class Query(ObjectType):

    vehicle = Field(NewCarModelType, slug=String())
    vehicles = List(NewCarModelType)
    makes = List(CarMakeType)
    make = Field(CarMakeType, slug=String(required=True))
    vehicles_by_make = List(NewCarModelType, slug=String(required=True))
    category_by_slug = Field(CategoryType, slug=String(required=True))
    category_all = List(CategoryType)
    popular_products = List(PopularProductByModelType, slug=String(required=True))

    def resolve_popular_products(self, info, slug):
        qs = Product.objects.filter(car_model__slug=slug).filter(
            product_image__isnull=False
        )[
            :20
        ]  # Needs to add some filter by popularity
        lst = []
        for prod in qs:
            models = [
                {
                    "id": x.id,
                    "slug": x.slug,
                    "model": x.name,
                    "make": {"slug": x.carmake.slug, "name": x.carmake.name},
                }
                for x in prod.car_model.all()
            ]
            bages = [{"name": x.name} for x in prod.bages.all()]
            images = [
                {
                    "img150x150": chk_img(x.img150x150),
                    "img245x245": chk_img(x.img245x245),
                    "img500x500": chk_img(x.img500x500),
                    "img150": chk_img(x.img500),
                    "img245": chk_img(x.img245),
                    "img500": chk_img(x.img500),
                    "main": x.main,
                }
                for x in prod.images
            ]
            lst.append(
                {
                    "id": prod.id,
                    "name": prod.name,
                    "slug": prod.slug,
                    "name2": prod.name2,
                    "full_name": prod.full_name,
                    "one_c_id": prod.one_c_id,
                    "sku": prod.sku,
                    "cat_number": prod.cat_number,
                    "model": models,
                    "images": images,
                    "bages": bages,
                }
            )

        return lst

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
        cat = Category.objects.filter(slug=slug).first()
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

    def resolve_vehicles_by_make(self, info, slug):
        qs = (
            CarModel.objects.filter(active=True)
            .filter(carmake__slug=slug)
            .annotate(count=Count("model_product"))
            .order_by("-priority")
        )
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
                    "priority": car.priority,
                    "make": {
                        "id": car.carmake.id,
                        "name": car.carmake.name,
                        "slug": car.carmake.slug,
                        "country": car.carmake.country,
                        "priority": car.carmake.priority,
                    },
                    "make_slug": car.carmake.slug,
                    "country": car.carmake.country,
                    "count": car.count,
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
        make = CarMake.objects.filter(slug=slug).first()
        return {
            "id": make.id,
            "name": make.name,
            "rusname": make.rusname,
            "slug": make.slug,
            "country": make.country.country,
            "priority": make.priority,
        }

    def resolve_vehicle(self, info, slug):
        car = CarModel.objects.filter(slug=slug).first()
        years = [car.year_from, car.year_to] if car.year_from else []
        return {
            "id": car.id,
            "model": car.name,
            "rusname": car.rusname,
            "year": years,
            "engine": car.engine.all(),
            "slug": car.slug,
            "priority": car.priority,
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
                    "priority": car.priority,
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
