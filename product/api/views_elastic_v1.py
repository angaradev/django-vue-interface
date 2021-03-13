from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product
import json, requests


def send_json(request):
    query = request.GET.get("q")
    if not query:
        query = 1
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
    data = response

    return JsonResponse(data, safe=False)
