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
    Mutation,
    DateTime,
)
from django.db.models import Count
from .utils import chk_img


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
    image = String(required=False)


class NewCarModelType(ObjectType):
    id = ID()
    model = String(required=False)
    rusname = String()
    year = List(String, required=True)
    engine = List(String, required=True)
    slug = String(required=True)
    make = Field(CarMakeType, required=True)
    country = String(required=True)
    priority = String()
    count = String()
    image = String(required=False)


class IProductImagesType(ObjectType):
    id = ID()
    img150 = String(required=False)
    img245 = String(required=False)
    img500 = String(required=False)
    img800 = String(required=False)
    img245x245 = String(required=False)
    img150x150 = String(required=False)
    img500x500 = String(required=False)
    img800x800 = String(required=False)
    main = Boolean(required=False)


class ProductStocksType(ObjectType):
    id = ID()
    store = String(required=False)
    price = Int(required=False)
    availability_days = Int(required=False)


class BrandType(ObjectType):
    id = ID()
    slug = String(required=False)
    name = String(required=False)
    country = String(required=False)
    image = String(required=False)


class PopularProductByModelType(ObjectType):
    id = ID()
    slug = String(required=True)
    name = String(required=True)
    name2 = String(required=False)
    full_name = String(required=False)
    one_c_id = String(required=False)
    sku = String(required=False)
    model = List(NewCarModelType, required=True)
    images = List(IProductImagesType)
    cat_number = String(required=True)
    bages = List(String, required=False)
    stocks = List(ProductStocksType, required=False)
    brand = Field(BrandType)


class EngineType(ObjectType):
    id = ID()
    name = String(required=False)
    image = String(required=False)


class AttributesType(ObjectType):
    name = String(required=False)
    value = String(required=False)


class RatingType(ObjectType):
    score = Int()
    autouser = String()
    product = ID()


class AutoUserType(ObjectType):
    userId = String()
    createdDate = DateTime()
    updatedDate = DateTime()


class GetRatingType(ObjectType):
    rating = Int()
    ratingCount = Int()


class ProductType(ObjectType):
    id = ID()
    slug = String(required=True)
    name = String(required=True)
    name2 = String(required=False)
    full_name = String(required=False)
    one_c_id = String(required=False)
    sku = String(required=False)
    active = Boolean(required=False)
    unit = String(required=False)
    cat_number = String(required=False)
    oem_number = String(required=False)
    partNumber = String(required=False)
    brand = Field(BrandType, required=False)
    related = List(String)
    category = List(CategoryType)
    model = List(NewCarModelType, required=False)
    engine = List(EngineType)
    excerpt = String(required=False)
    description = String(required=False)
    created_date = Date(required=False)
    updated_date = Date(required=False)
    has_photo = Boolean(required=True)
    images = List(IProductImagesType, required=False)
    attributes = List(AttributesType)
    stocks = List(ProductStocksType, required=False)
    bages = List(String, required=False)
    rating = Int()
    ratingCount = Int()
    video = List(String)
    condition = String(required=False)
