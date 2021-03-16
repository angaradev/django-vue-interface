from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests


def send_json(request):
    query = request.GET.get("q").lower()
    if not query:
        query = "hd78"
    if query == "all":
        data = json.dumps(
            {
                "query": {"match_all": {}},
                "aggs": {
                    "categories": {"terms": {"field": "category.id", "size": 2000}},
                    "brands": {"terms": {"field": "brand.name.keyword"}},
                    "engines": {"terms": {"field": "engine.name.keyword"}},
                    "car_models": {"terms": {"field": "model.name.keyword"}},
                    "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                },
            }
        )
    else:
        data = json.dumps(
            {
                "size": 0,
                "query": {"term": {"model.name.keyword": query}},
                "aggs": {
                    "categories": {"terms": {"field": "category.id", "size": 2000}},
                    "brands": {"terms": {"field": "brand.name.keyword"}},
                    "engines": {"terms": {"field": "engine.name.keyword"}},
                    "car_models": {"terms": {"field": "model.name.keyword"}},
                    "bages": {"terms": {"field": "bages.keyword", "size": 5}},
                },
            }
        )

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
