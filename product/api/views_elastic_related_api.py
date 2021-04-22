from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint, re

pp = pprint.PrettyPrinter(indent=2)

#
# Searching for similar products by car and name of part
#
def similar(request):
    if request.method == "GET":
        q = request.GET.get("q")
        model = request.GET.get("model")
        """
        Check if search by make slug exists
        """

        if model and q:

            # If query has car model and slug
            query = {
                "size": 20,
                "_source": ["id", "name"],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"model.slug.keyword": model}},
                            {
                                "match": {
                                    "name": {
                                        "query": q,
                                        "analyzer": "rebuilt_russian",
                                        "fuzziness": "auto",
                                        "operator": "and",
                                    }
                                }
                            },
                        ]
                    }
                },
            }
            data = json.dumps(query)

        r = requests.get(
            "http://localhost:9200/prod_notebook/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        if r.status_code != 200:
            raise ValueError(
                f"Request cannot be proceeded Status code is: {r.status_code}"
            )
        response = r.json()

        # Cheking if aggregation exist in the query

        data = response

        return JsonResponse(data, safe=False)

    else:
        raise Exception({"Cannot poceed the request, params are suck"})
