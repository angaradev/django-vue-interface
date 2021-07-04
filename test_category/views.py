from django.shortcuts import render
from django.http import HttpResponse
from test_category.elastic_insert import do_all
from django.conf import settings
import requests, json
import os

# Create your views here.
def elastic_file_create(request):
    try:
        prods = True  # do_all()
        # prods = do_all()
        if prods:

            # Deleting index
            # requests.delete(f"{settings.ELASTIC_URL}/prod_notebook")

            # # Mapping index
            # m = open(
            #     os.path.join(
            #         settings.BASE_DIR, "test_category", "product_mapping.json"
            #     ),
            #     "r",
            # )

            # requests.put(
            #     f"{settings.ELASTIC_URL}/prod_notebook",
            #     headers={"Content-Type": "application/json"},
            #     data=json.load(m),
            # )
            f = open(
                os.path.join(settings.BASE_DIR, "product_notebook.json"),
                "r",
                encoding="utf-8",
            )
            data = json.load(f)
            print(data)
            r = requests.post(
                f"{settings.ELASTIC_URL}/prod_notebook",
                headers={"Content-Type": "application/x-ndjson"},
                data=f,
            )
        return HttpResponse(f"<h1>Created {prods} Products so far</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Somethin went wrong {e}</h1>")


# curl -H 'Content-Type: application/x-ndjson' -XDELETE 'http://localhost:9200/prod_notebook';
# curl -H 'Content-Type: application/x-ndjson' -XPUT 'http://localhost:9200/prod_notebook'
# --data-binary @/home/manhee/Projects/quora/quora/test_category/product_mapping.json;
# curl -H 'Content-Type: application/x-ndjson' -XPUT 'http://localhost:9200/_bulk' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_notebook.txt > el_log.txt;
