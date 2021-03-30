from django.views.generic.base import TemplateView
from django.http import JsonResponse
from product.models import Product, Category
import json, requests
import pprint

pp = pprint.PrettyPrinter(indent=2)


def aggs(size):
    aggs = {
        "categories": {"terms": {"field": "category.id", "size": size}},
        "brands": {"terms": {"field": "brand.name.keyword"}},
        "engines": {"terms": {"field": "engine.name.keyword"}},
        "car_models": {"terms": {"field": "model.name.keyword"}},
        "bages": {"terms": {"field": "bages.keyword", "size": 5}},
        "min_price": {"min": {"field": "stocks.price"}},
        "max_price": {"max": {"field": "stocks.price"}},
    }
    return aggs


def make_query(request, aggs, aggs_size, product_sizes=2000):
    query = []
    sub = []
    subf = []

    for item in request.GET.items():
        if str(item[0]) == "price":
            continue
        # must here
        second = item[1].split(",")
        if len(second) > 1:
            sub.append({"filter": item[0], "items": [*second]})

        # First level for
        if item[0] == "model" or item[0] == "category":

            query.append(
                {"term": {f"{item[0]}.slug.keyword": second[0]}},
            )
        for l in sub:
            print(l)
            for it in l["items"]:
                if l["filter"] == "brand":
                    subf.append({"term": {f"{l['filter']}.name.keyword": it}})
                else:
                    subf.append({"term": {f"{l['filter']}.slug.keyword": it}})

    tmp = {
        "size": product_sizes,
        "query": {
            "bool": {
                "must": [
                    *query,
                    {"bool": {"should": subf}},
                ]
            }
        },
        "aggs": aggs(aggs_size),
    }

    pp.pprint(tmp)

    # with open("/home/manhee/Projects/quora/quora/test_category/sample.json", "w") as f:
    #     json.dump(tmp, f, indent=2)
    # f.close()

    return json.dumps(tmp)


def send_json(request):
    aggs_size = 2000
    product_sizes = 200
    if request.method == "GET":
        """
        Check if search by make slug exists
        """

        cat = request.GET.get("category")
        model = request.GET.get("model")
        make = request.GET.get("make")
        brand = request.GET.getlist("brand")
        data = None

        if model and cat and not make and len(request.GET.keys()) > 2:
            print("IN make models and filters")
            data = make_query(request, aggs, aggs_size, product_sizes)

        if model and cat and brand:
            print("In model cat and brand")

            # needs to rerfactor to helper
            query = []
            for item in brand:
                query.append(
                    {"term": {"brand.name.keyword": item.lower()}},
                )

            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"model.slug.keyword": model}},
                                {"term": {"category.slug.keyword": cat}},
                                {"bool": {"should": query}},
                            ]
                        }
                    },
                    # here goes aggs
                    "aggs": aggs(aggs_size),
                }
            )

        if make and not model and not cat:
            print("in make not model not cat")

            makeSlug = make.lower()
            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {"term": {"model.make.slug.keyword": makeSlug}},
                    "aggs": aggs(aggs_size),
                }
            )

            # If query has query and car model
        if model and not cat and not make:
            print("In model not cat not make")
            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {"term": {"model.slug.keyword": model}},
                    "aggs": aggs(aggs_size),
                }
            )
        # If query has car model and slug
        if model and cat and not make and not brand:
            print("In model and cat")
            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"model.slug.keyword": model}},
                                {"term": {"category.slug.keyword": cat}},
                            ]
                        }
                    },
                    "aggs": aggs(aggs_size),
                }
            )

        # if query has q == 'all'
        if model == "all" and not cat:
            print("In all statement")
            data = json.dumps(
                {
                    "size": product_sizes,
                    "query": {"match_all": {}},
                    "aggs": aggs(aggs_size),
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


def send_json_filters(request):
    aggs_size = 2000
    product_sizes = 200
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
                    "size": product_sizes,
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
                    "size": product_sizes,
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
                        "size": product_sizes,
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
                        "size": product_sizes,
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
                        "size": product_sizes,
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
