from product.models.models import ProductRating
import math
from functools import reduce
from django.db.models import Avg, Q
from users.models import AutoUser
from product.models import CarModel, CarMake, Category, Product
from graphene import (
    String,
    ObjectType,
    Date,
    ID,
    Field,
    Schema,
    List,
    Boolean,
    Int,
    DateTime,
)
from django.db.models import Count
from .utils import chk_img
from .schemaTypes import *
from .schemaMutations import Mutation
from .utils import stemmer


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
# esh = Elasticsearch(["http://localhost:9200"])
class ratingAvgType(ObjectType):
    ratingAvg = Int()


def ratingAvg(productId):
    try:
        product = Product.objects.get(id=productId)
        qs = ProductRating.objects.filter(product=product)
        avg = qs.aggregate(avg_score=Avg("score"))
        count = qs.count()

        return math.ceil(avg["avg_score"]), count
    except Exception as e:
        return None, None


class Query(ObjectType):

    vehicle = Field(NewCarModelType, slug=String())
    vehicles = List(NewCarModelType)
    makes = List(CarMakeType)
    make = Field(CarMakeType, slug=String(required=True))
    vehicles_by_make = List(NewCarModelType, slug=String(required=True))
    category_by_slug = Field(CategoryType, slug=String(required=True))
    category_all = List(CategoryType)
    popular_products = List(
        PopularProductByModelType,
        slugs=List(String),
        quantity=Int(required=True),
    )
    similarProducts = List(ProductType, slug=String(required=True), quantity=Int())
    product = Field(ProductType, slug=String(required=True))
    autouser = Field(AutoUserType, userId=String(required=True))
    rating = Field(RatingType, productId=Int(), userId=String())
    productRating = Field(GetRatingType, productId=Int())
    analogs = List(ProductType, catNumber=String(), productId=Int())

    def resolve_similarProducts(self, info, slug, quantity):
        try:
            product = Product.objects.get(slug=slug)
            searchWords = stemmer(product.name)
            query = reduce(
                lambda q, value: q & Q(name__icontains=value), searchWords[:1], Q()
            )
            models = [x.slug for x in product.car_model.all()]

            similar = (
                Product.objects.filter(car_model__slug__in=models)
                .filter(query)
                .exclude(id=product.id)[:quantity]
            )
            returnProductList = []
            for prod in similar:
                models = [
                    {
                        "id": x.id,
                        "slug": x.slug,
                        "name": x.name,
                        "model": x.name,
                        "priority": x.priority,
                        "image": x.image.url if x.image else None,
                        "rusname": x.rusname,
                        "make": {
                            "slug": x.carmake.slug,
                            "name": x.carmake.name,
                            "id": x.carmake.id,
                            "country": x.carmake.country,
                        },
                    }
                    for x in prod.car_model.all()
                ]
                engines = [
                    {
                        "id": x.id,
                        "name": x.name,
                        "image": x.image.url if x.image else None,
                    }
                    for x in prod.engine.all()
                ]
                stocks = [
                    {
                        "price": x.price,
                        "quantity": x.quantity,
                        "store": {"id": x.store.id, "name": x.store.name},
                    }
                    for x in prod.product_stock.all()
                ]
                images = [
                    {
                        "img150": x.img150.url if x.img150 else None,
                        "img245": x.img245.url if x.img245 else None,
                        "img500": x.img500.url if x.img500 else None,
                        "img800": x.img800.url if x.img800 else None,
                        "img150x150": x.img150x150.url if x.img150x150 else None,
                        "img245x245": x.img245.url if x.img245x245 else None,
                        "img500x500": x.img500x500 if x.img500x500 else None,
                        "img800x800": x.img800x800 if x.img800x800 else None,
                        "main": x.main,
                    }
                    for x in prod.images.all()
                ]
                returnProduct = {
                    "id": prod.id,
                    "slug": prod.slug,
                    "name": prod.name,
                    "name2": prod.name2,
                    "full_name": prod.full_name,
                    "one_c_id": prod.one_c_id,
                    "sku": prod.sku,
                    "active": prod.active,
                    "uint": prod.unit,
                    "cat_number": prod.cat_number,
                    "oem_number": prod.oem_number,
                    "images": images,
                    "partNumber": prod.partNumber,
                    "brand": {
                        "id": prod.brand.id,
                        "slug": prod.brand.slug,
                        "name": prod.brand.brand,
                        "country": prod.brand.country,
                        "image": prod.brand.image,
                    },
                    "stocks": stocks,
                    "bages": prod.bages,
                    "rating": ratingAvg(prod.id)[0],
                    "ratingCount": ratingAvg(prod.id)[1],
                    "condition": prod.condition,
                    "model": models,
                    "engine": engines,
                }
                returnProductList.append(returnProduct)
            return returnProductList
        except Exception as e:
            print(e)
            return []

    def resolve_analogs(self, info, catNumber, productId):
        qs = Product.objects.filter(cat_number=catNumber).exclude(id=productId)
        returnProductList = []
        for prod in qs:
            stocks = [
                {
                    "price": x.price,
                    "quantity": x.quantity,
                    "store": {"id": x.store.id, "name": x.store.name},
                }
                for x in prod.product_stock.all()
            ]
            returnProduct = {
                "id": prod.id,
                "slug": prod.slug,
                "name": prod.name,
                "name2": prod.name2,
                "full_name": prod.full_name,
                "one_c_id": prod.one_c_id,
                "sku": prod.sku,
                "active": prod.active,
                "uint": prod.unit,
                "cat_number": prod.cat_number,
                "oem_number": prod.oem_number,
                "partNumber": prod.partNumber,
                "brand": {
                    "id": prod.brand.id,
                    "slug": prod.brand.slug,
                    "name": prod.brand.brand,
                    "country": prod.brand.country,
                    "image": prod.brand.image,
                },
                "stocks": stocks,
                "bages": prod.bages,
                "rating": ratingAvg(prod.id)[0],
                "ratingCount": ratingAvg(prod.id)[1],
                "condition": prod.condition,
            }
            returnProductList.append(returnProduct)
        return returnProductList

    def resolve_productRating(self, info, productId):
        try:
            product = Product.objects.get(id=productId)
            rating = ProductRating.objects.filter(product=product)
            count = rating.count()
            avg = rating.aggregate(avg_score=Avg("score"))
            return {"rating": avg["avg_score"], "ratingCount": count}

        except:
            return {"rating": None, "ratingCoung": None}

    def resolve_rating(self, info, productId, userId):
        try:
            product = Product.objects.get(id=productId)
            qs = ProductRating.objects.get(product=product, autoUser__userId=userId)
            return qs
        except:
            return None

    def resolve_autouser(self, info, userId):
        qs = AutoUser.objects.get(userId=userId)
        return {
            "userId": qs.userId,
            "createdDate": qs.created_date,
            "updatedDate": qs.updated_date,
        }

    def resolve_popular_products(self, info, slugs, quantity=20):
        qs = (
            Product.objects.filter(car_model__slug__in=slugs)
            .filter(product_image__isnull=False)
            .distinct()[:quantity]
        )  # Needs to add some filter by popularity
        lst = []
        for prod in qs:
            models = [
                {
                    "id": x.id,
                    "slug": x.slug,
                    "model": x.name,
                    "image": x.image.url if x.image else None,
                    "make": {"slug": x.carmake.slug, "name": x.carmake.name},
                }
                for x in prod.car_model.all()
            ]
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
            stocks = [
                {
                    "id": x.id,
                    "store": {
                        "name": x.store.name,
                        "location_city": x.store.location_city,
                    },
                    "price": x.price,
                    "quantity": x.quantity,
                    "availability_days": x.availability_days,
                }
                for x in prod.product_stock.all()
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
                    "bages": prod.bages,
                    "stocks": stocks,
                    "brand": {"name": prod.brand.brand, "conuntry": prod.brand.country},
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
                    "image": car.image.url if car.image else None,
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
                    "image": make.image.url if make.image else None,
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
            "image": make.image.url if make.image else None,
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
            "image": car.image.url if car.image else None,
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
                    "image": car.image.url if car.image else None,
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

    def resolve_product(self, info, slug):

        prod = Product.objects.get(slug=slug)
        cats = [
            {
                "id": x.id,
                "name": x.name,
                "slug": x.slug,
                "parent": x.parent.id,
            }
            for x in prod.category.all()
        ]

        models = [
            {
                "id": x.id,
                "slug": x.slug,
                "name": x.name,
                "model": x.name,
                "priority": x.priority,
                "image": x.image.url if x.image else None,
                "rusname": x.rusname,
                "make": {
                    "slug": x.carmake.slug,
                    "name": x.carmake.name,
                    "id": x.carmake.id,
                    "country": x.carmake.country,
                },
            }
            for x in prod.car_model.all()
        ]
        engines = [
            {
                "id": x.id,
                "name": x.name,
                "image": x.image.url if x.image else None,
            }
            for x in prod.engine.all()
        ]
        images = [
            {
                "img150": x.img150.url if x.img150 else None,
                "img245": x.img245.url if x.img245 else None,
                "img500": x.img500.url if x.img500 else None,
                "img800": x.img800.url if x.img800 else None,
                "img150x150": x.img150x150.url if x.img150x150 else None,
                "img245x245": x.img245.url if x.img245x245 else None,
                "img500x500": x.img500x500 if x.img500x500 else None,
                "img800x800": x.img800x800 if x.img800x800 else None,
                "main": x.main,
            }
            for x in prod.images.all()
        ]
        attrs = [
            {"name": x.attribute_name.name, "value": x.attribute_value}
            for x in prod.product_attribute.all()
        ]
        stocks = [
            {
                "price": x.price,
                "quantity": x.quantity,
                "store": {"id": x.store.id, "name": x.store.name},
            }
            for x in prod.product_stock.all()
        ]

        returnProduct = {
            "id": prod.id,
            "slug": prod.slug,
            "name": prod.name,
            "name2": prod.name2,
            "full_name": prod.full_name,
            "one_c_id": prod.one_c_id,
            "sku": prod.sku,
            "active": prod.active,
            "uint": prod.unit,
            "cat_number": prod.cat_number,
            "oem_number": prod.oem_number,
            "partNumber": prod.partNumber,
            "brand": {
                "id": prod.brand.id,
                "slug": prod.brand.slug,
                "name": prod.brand.brand,
                "country": prod.brand.country,
                "image": prod.brand.image,
            },
            "related": [x.id for x in prod.related.all()],
            "category": cats,
            "model": models,
            "engine": engines,
            "excerpt": prod.excerpt,
            "description": prod.description,
            "created_date": prod.created_date,
            "updated_date": prod.updated_date,
            "has_photo": prod.have_photo,
            "images": images,
            "video": [x.url for x in prod.product_video.all()],
            "attributes": attrs,
            "stocks": stocks,
            "bages": prod.bages,
            "rating": ratingAvg(prod.id)[0],
            "ratingCount": ratingAvg(prod.id)[1],
            "condition": prod.condition,
        }
        return returnProduct


schema = Schema(query=Query, mutation=Mutation)
