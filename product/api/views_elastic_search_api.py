from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint, re, os
from django.conf import settings

pp = pprint.PrettyPrinter(indent=2)
autocomplete_size = 14

main_params = ["model", "category"]
filters_params = [
    "brand",
    "engine",
    "bages",
    "price",
    "image",
    "has_photo",
    "condition",
]


def aggs(size):
    aggs = {
        "categories": {"terms": {"field": "category.id", "size": size}},
        "brands": {"terms": {"field": "brand.name.keyword"}},
        "engines": {"terms": {"field": "engine.name.keyword"}},
        "car_models": {"terms": {"field": "model.name.keyword"}},
        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
        "condition": {"terms": {"field": "condition.keyword", "size": 5}},
        "min_price": {"min": {"field": "stocks.price"}},
        "max_price": {"max": {"field": "stocks.price"}},
        "has_photo": {"terms": {"field": "has_photo"}},
    }
    return aggs


def make_query(request, aggs, aggs_size, category=False, page_from=1, page_size=200):
    query = []
    boolShould = []
    price = request.GET.get("price")
    priceMin = 1
    priceMax = 10000000
    search = request.GET.get("search")
    sort_price = request.GET.get("sort_price") or "asc"
    if price:
        spl = price.split("-")
        priceMin = spl[0]
        priceMax = spl[1]

    for item in request.GET.items():
        if item[0] == "sort_price":
            continue
        if str(item[0]) == "page_from" or str(item[0]) == "page_size":
            continue
        # must here
        second = item[1].split(",")
        if item[0] == "search":
            # If search is a number
            if re.match(r"^\d+", str(search)):
                print(search)

                query.append(
                    {
                        "match": {
                            "cat_number": {
                                "query": search,
                                "analyzer": "standard",
                            }
                        },
                    }
                )
            # Else search is a text

            else:
                query.append(
                    {
                        "match": {
                            "full_name_ngrams": {
                                "query": second[0],
                                "operator": "and",
                                "analyzer": "rebuilt_russian",
                                "fuzziness": "auto",
                            }
                        }
                    }
                )
                # query.append(
                #     {
                #         "match": {
                #             "full_name": {
                #                 "query": second[0],
                #                 "operator": "and",
                #                 "fuzziness": "auto",
                #             }
                #         }
                #     },
                # )

        inside = []  # var for collecting inner filter values
        if str(item[0]) != "search":
            for filVal in second:
                if str(item[0]) == "price":
                    # adding range here
                    lst = {
                        "range": {"stocks.price": {"gte": priceMin, "lte": priceMax}}
                    }

                elif item[0] == "category" or item[0] == "condition":
                    lst = {"term": {f"{item[0]}.slug.keyword": filVal}}
                elif item[0] == "car_models":
                    lst = {"term": {"model.name.keyword": filVal}}
                elif item[0] == "condition":
                    lst = {"term": {f"{item[0]}.slug.keyword": filVal}}
                elif item[0] == "bages" or item[0] == "condition":
                    lst = {"term": {f"{item[0]}.keyword": filVal}}
                elif item[0] == "has_photo":
                    phot = "false"
                    if filVal == "0":
                        phot = "false"
                    else:
                        phot = "true"
                    lst = {"term": {"has_photo": phot}}
                else:
                    lst = {"term": {f"{item[0]}.name.keyword": filVal}}
                inside.append(lst)
            # pp.pprint(inside)

            subitem = {"bool": {"should": [x for x in inside]}}
            boolShould.append(subitem)
            pp.pprint(subitem)

    tmp = {
        "from": page_from,
        "size": page_size,
        "sort": [{"stocks.price": {"order": sort_price}}],
        "query": {
            "bool": {
                "must": [
                    *query,
                    {"bool": {"must": boolShould}},
                ]
            }
        },
        "aggs": aggs(aggs_size),
    }

    # pp.pprint(tmp)

    with open(os.path.join(settings.BASE_DIR, "test_category/sample.json"), "w") as f:
        json.dump(tmp, f, indent=2)
    f.close()

    return json.dumps(tmp)


# Function for checking if filters in defined list exists in qyery params
def checFilters(filters, get):
    flag = False

    for item in get:
        if item in filters:
            flag = True
            break
    return flag


def send_json(request):
    aggs_size = 2000
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        page_size = request.GET.get("page_size") or 200

        page_from = request.GET.get("page_from") or 0
        search = request.GET.get("search") or None

        cat = request.GET.get("category")
        model = request.GET.get("model")
        make = request.GET.get("make")
        data = None
        q_list = [x[0] for x in request.GET.items()]
        filters_chk = checFilters(filters_params, q_list)

        data = make_query(request, aggs, aggs_size, True, page_from, page_size)

        # If query has car model and slug

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


def autocomplete(request):
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        q = request.GET.get("q")

        # If query has car model and slug
        # query = {"size": "20", "query": {"prefix": {"full_name": {"value": q}}}}
        query = {
            "size": autocomplete_size,
            "_source": ["id", "name"],
            "query": {
                "match": {
                    "name": {
                        "query": q,
                        "analyzer": "rebuilt_russian",
                        "fuzziness": "auto",
                        "operator": "and",
                    }
                }
            },
        }
        if request.GET.get("model"):

            query = {
                "size": autocomplete_size,
                "_source": ["id", "name"],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"model.slug.keyword": "porter1"}},
                            {
                                "match": {
                                    "name": {
                                        "query": "помпа портер насос",
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

    r = requests.get(
        "http://localhost:9200/prod_notebook/_search",
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )
    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    data = response

    return JsonResponse(data, safe=False)


def findNumbers(request):
    if request.method == "GET":
        """
        Check if search by make slug exists
        """
        q = request.GET.get("q")

        # If query has car model and slug
        # query = {"size": "20", "query": {"prefix": {"full_name": {"value": q}}}}
    query = {
        "query": {"match": {"cat_number": {"query": q, "analyzer": "standard"}}},
    }

    r = requests.get(
        "http://localhost:9200/prod_notebook/_search",
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )
    if r.status_code != 200:
        raise ValueError(f"Request cannot be proceeded Status code is: {r.status_code}")
    response = r.json()

    data = response

    return JsonResponse(data, safe=False)
