from product.syncronizators.products_sync import sync_products
from test_category.elastic_insert import do_all_two
from test_category.elastic_stuff2 import do_insert
from product.syncronizators.prices_sync import update_prices


def do_all_products():
    print("Start syncing products")
    try:
        sync_products()
    except Exception as e:
        print(e)
    print("Start making elastic base")
    do_all_two()
    print("Start inserting elastic base")
    do_insert()
    print("Starting update prices")
    update_prices()
    print("All stuff finished")
