from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests


def send_json(request):
    query = request.GET.get("q")
    if not query:
        query = 1
    data_aggs = json.dumps(
        {
            "size": 0,
            "query": {"match": {"categories.cat_parent": query}},
            "aggs": {
                "categories": {"terms": {"field": "categories.cat_id"}},
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

    categories = response["aggregations"]["categories"]["buckets"]
    rebuilt_cats = []
    for category in categories:
        new_cat = Category.objects.get(id=category["key"])
        rebuilt_cats.append(
            {
                "key": category["key"],
                "doc_count": category["doc_count"],
                "id": new_cat.id,
                "name": new_cat.name,
                "parent": new_cat.parent_id,
                "layout": new_cat.layout,
                "type": new_cat.type,
            }
        )
    response["aggregations"]["categories"]["buckets"] = rebuilt_cats

    data = response

    return JsonResponse(data, safe=False)
