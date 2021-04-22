from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint, re

pp = pprint.PrettyPrinter(indent=2)


def similar(request):
    if request.method == "GET":
        q = request.GET.get("q")
        pp.pprint(q)
        """
        Check if search by make slug exists
        """

        # If query has car model and slug
        query = {
            "size": 20,
            "_source": ["id", "name"],
            "query": {
                "match": {
                    "name": {
                        "query": "string",
                        "analyzer": "rebuilt_russian",
                        "fuzziness": "auto",
                        "operator": "and",
                    }
                }
            },
        }

    r = requests.get(
        "http://localhost:9200/prod_notebook/_search",
        headers={"Content-Type": "application/json"},
        data=query,
    )
    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    # Cheking if aggregation exist in the query

    data = response

    return JsonResponse(data, safe=False)
