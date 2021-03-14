from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests


def send_json(request):
    query = request.GET.get("q")
    if not query:
        query = 1
    data = json.dumps({"query": {"match_all": {}}})
    data_aggs = json.dumps(
        {
            "size": 0,
            "query": {"term": {"car_model.model_name.keyword": "HD78"}},
            "aggs": {
                "categories": {"terms": {"field": "categories.cat_id", "size": 100}},
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
