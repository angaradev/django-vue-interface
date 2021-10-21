from django.conf import settings
import requests, os


def do_insert():
    headers = {"Content-Type": "application/x-ndjson"}
    working_dir = os.path.join(settings.BASE_DIR, "test_category")
    path = os.path.join(working_dir, "product_mapping.json")

    with open(path, "r", encoding="utf-8") as file_mapping:
        data_mapping = file_mapping.read()

    path_insert = os.path.join(working_dir, "product_notebook2.txt")
    file_insert = open(path_insert, "r")
    with open(path_insert, "r", encoding="utf-8") as data_insert:
        data_insert = file_insert.read()

    res_delete = requests.delete("http://localhost:9200/prod_all", headers=headers)
    res_mapping = requests.put(
        "http://localhost:9200/prod_all",
        data=data_mapping.encode("utf-8"),
        headers=headers,
    )
    res_insert = requests.put(
        "http://localhost:9200/_bulk",
        data=data_insert.encode("utf-8"),
        headers=headers,
    )
    print(res_delete, res_mapping, res_insert)


# curl -H 'Content-Type: application/x-ndjson' -XDELETE 'http://localhost:9200/prod_all';
# curl -H 'Content-Type: application/x-ndjson' -XPUT \
#   'http://localhost:9200/prod_all' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_mapping.json;
# curl -H 'Content-Type: application/x-ndjson' -XPUT \
#   'http://localhost:9200/_bulk' --data-binary @/home/manhee/Projects/quora/quora/test_category/product_notebook2.txt > el_log.log;
