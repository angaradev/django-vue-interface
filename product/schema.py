from test_category.models.vehicle_models import Engine
from product.models.models import CarMake, CarModel
from graphene import String, ObjectType, Int, ID, Field, Schema, Interface, List
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch import Elasticsearch
import requests, json


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
es = Elasticsearch(["http://localhost:9200"])


class EngineType(DjangoObjectType):
    class Meta:
        model = Engine
        fields = ("name",)


class CarMakeType(DjangoObjectType):
    class Meta:
        model = CarMake
        fields = ("name", "country")


class CarModelType(DjangoObjectType):
    class Meta:
        model = CarModel
        fields = ("name", "engine", "carmake", "slug")


class Query(ObjectType):

    vehicle = List(CarModelType)

    def resolve_vehicle(root, info):
        return CarModel.objects.all()


schema = Schema(query=Query)
