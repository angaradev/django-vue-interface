from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests


def send_json(request):
    aggs_size = 2000
    cat_slug = None
    query = None
    makeSlug = None
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        if request.GET.get("makeSlug"):

            makeSlug = request.GET.get("makeSlug")
            makeSlug = makeSlug.lower()
            data = json.dumps(
                {
                    "size": 10,
                    "query": {"term": {"model.make.slug.keyword": makeSlug}},
                    "aggs": {
                        "unique_ids": {"terms": {"field": "id"}},
                        "categories": {
                            "terms": {"field": "category.id", "size": aggs_size}
                        },
                        "brands": {"terms": {"field": "brand.name.keyword"}},
                        "engines": {"terms": {"field": "engine.name.keyword"}},
                        "car_models": {"terms": {"field": "model.name.keyword"}},
                        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                    },
                }
            )

        else:
            """
            Here starts parts if no query by makeSlug search
            """
            if request.method == "GET":
                if request.GET.get("q") == "all":
                    print(
                        "\033[93m",
                        "Attention ALL PRODUCTS REQUEST PERFORMED!",
                        request.GET,
                    )
                if "q" in request.GET:
                    query = request.GET["q"].lower()
                if "cat" in request.GET:
                    cat_slug = request.GET["cat"].lower()

            data = json.dumps(
                {
                    "size": 10,
                    "query": {"match_all": {}},
                    "aggs": {
                        "unique_ids": {"terms": {"field": "id"}},
                        "categories": {
                            "terms": {"field": "category.id", "size": aggs_size}
                        },
                        "brands": {"terms": {"field": "brand.name.keyword"}},
                        "engines": {"terms": {"field": "engine.name.keyword"}},
                        "car_models": {"terms": {"field": "model.name.keyword"}},
                        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                    },
                }
            )

            # If query has query and car model
            if query and not cat_slug:
                data = json.dumps(
                    {
                        "size": 10,
                        "query": {"term": {"model.slug.keyword": query}},
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": aggs_size}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )
            # If query has car model and slug
            if query and cat_slug:
                data = json.dumps(
                    {
                        "size": 10,
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"model.slug.keyword": query}},
                                    {"term": {"category.slug.keyword": cat_slug}},
                                ]
                            }
                        },
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": aggs_size}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )

            # if query has q == 'all'
            if query == "all" and not cat_slug:
                data = json.dumps(
                    {
                        "size": 10,
                        "query": {"match_all": {}},
                        "aggs": {
                            "unique_ids": {"terms": {"field": "id"}},
                            "categories": {
                                "terms": {"field": "category.id", "size": 2000}
                            },
                            "brands": {"terms": {"field": "brand.name.keyword"}},
                            "engines": {"terms": {"field": "engine.name.keyword"}},
                            "car_models": {"terms": {"field": "model.name.keyword"}},
                            "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                        },
                    }
                )
            # if query has q == all and cat slug

    r = requests.get(
        "http://localhost:9200/prod_notebook/_search",
        headers={"Content-Type": "application/json"},
        data=data,
    )
    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    # Cheking if aggregation exist in the query
    if "aggregations" in response:
        categories = response["aggregations"]["categories"]["buckets"]
        rebuilt_cats = []
        for category in categories:
            new_cat = None
            try:
                new_cat = Category.objects.get(id=category["key"])
            except Exception as e:
                print("Error in replace categories in elasticsearc", e)
                print("key does not exists: ", category["key"])
            rebuilt_cats.append(
                {
                    "id": category["key"],
                    "count": category["doc_count"],
                    "id": new_cat.id,
                    "name": new_cat.name,
                    "parent": new_cat.parent_id,
                    "layout": new_cat.layout,
                    "type": new_cat.type,
                    "slug": new_cat.slug,
                }
            )
        response["aggregations"]["categories"]["buckets"] = rebuilt_cats

    data = response

    return JsonResponse(data, safe=False)
