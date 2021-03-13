from graphene import String, ObjectType, Int, ID, Field, Schema, Interface, List
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
import requests, json
from .schemas.GraphqlInterfaces import *
from .schemas.ProductSchema import *


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
es = Elasticsearch(["http://localhost:9200"])


class Query(ObjectType):

    root = Field(Root, query=String())

    def resolve_root(root, info, query):
        # data = json.dumps(
        #     {"size": 1000, "query": {"term": {"car_model.model_name.keyword": query}}}
        # )
        data_aggs = json.dumps(
            {
                "size": 20,
                "query": {"match": {"categories.cat_parent": query}},
                "aggs": {
                    "categories": {"terms": {"field": "categories.cat_name.keyword"}},
                    "brands": {"terms": {"field": "brand.brand_name.keyword"}},
                    "engines": {"terms": {"field": "engines.engine_name.keyword"}},
                    "car_models": {"terms": {"field": "car_model.model_name.keyword"}},
                },
            }
        )

        r = requests.get(
            "http://localhost:9200/prod_notebook/_search",
            headers={"Content-Type": "application/json"},
            data=data_aggs,
        )
        response = r.json()

        products = response["hits"]["hits"]
        aggs = response["aggregations"]

        return {"product": products, "aggregations": aggs}

    elastic = String()

    def resolve_elastic(root, info):
        return f"this is elastic"


schema = Schema(query=Query)
