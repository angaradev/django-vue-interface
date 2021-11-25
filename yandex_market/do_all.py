from yandex_market.yandex_market_api.yandex_market_update import (
    do_all_update_prices as y_price,
)
from yandex_market.yandex_market_api.yandex_market_update import (
    do_all_update_products as y_products,
)
from yandex_market.ozon_api.ozon_update import do_all_update_products as oz_products
from yandex_market.ozon_api.ozon_update import stocks_update as oz_stock


def update_all_marktplaces():
    y_products(True, 0)
    y_price(True)
    oz_products(True, 0)
    oz_stock(True, 0)
