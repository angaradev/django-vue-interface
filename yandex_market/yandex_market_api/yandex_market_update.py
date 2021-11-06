import os, math
from quora.common_lib.logger import logger
import re
import pathlib
from bs4 import BeautifulSoup
from quora.local_settings import OAUTH_YANDEX_MARKET
from product.models import Product
from django.conf import settings
import requests, json, time
from django.core.mail import send_mail
from quora.common_lib.get_parent_category import parent_category
from quora.common_lib.get_or_make_description import clear_description


maslo_ids = [3226, 25489, 25484, 23704, 25485, 23781]


def get_cat(product):
    for cat in product.category.all():
        for inn_cat in cat.get_ancestors(include_self=False):
            yc = inn_cat.yandex_category.name
            if yc:
                return yc


def chunkGenerator(chunk_size):
    # Chunk size
    n = chunk_size
    # Select products with images and prices
    oils = Product.objects.filter(one_c_id__in=maslo_ids).distinct()
    products_tmp = (
        Product.objects.filter(product_image__img150__isnull=False)
        .filter(product_stock__quantity__gt=0)
        .distinct()
    )
    products = oils | products_tmp
    print("Products selected:", products.count())
    for i in range(0, products.count(), n):
        yield products[i : i + n]


def makeProduct(product):
    imgUrl = "https://angara77.ru"  # settings.SITE_URL
    siteUrl = "https://partshub.ru"  # settings.SITE_URL

    name = product.make_name

    brand = "MOBIS"
    try:

        brand = product.brand.brand.upper()
        if not brand or brand == "оригинал":
            brand = "MOBIS"
    except Exception as e:
        # print("No brand found")
        pass

    default_country = "Южная Корея"
    country = None
    try:
        country = (
            product.brand.country.upper() if product.brand.country else default_country
        )
    except Exception as e:
        # print("No counnreis found")
        country = default_country
    images = []
    try:
        images = [f"{imgUrl}{x.img800.url}" for x in product.product_image.all()]
    except Exception as e:
        # print(e)
        pass

    category = get_cat(product) or "Запчасти"

    description = clear_description(product)

    testProduct = None

    try:

        testProduct = {
            "offer": {
                "shopSku": product.one_c_id,
                "name": name,
                "category": category,
                "manufacturer": brand,
                "manufacturerCountries": [country],
                "description": description,
                "weightDimensions": {
                    "length": 15.0,
                    "width": 24.0,
                    "height": 12.5,
                    "weight": 3.1,
                },
                "urls": [f"{siteUrl}/product/{product.slug}"],
                "pictures": images,
                "vendor": brand,
                "vendorCode": product.cat_number,
                "shelfLife": {"timePeriod": 5, "timeUnit": "YEAR"},
                "minShipment": 1,
                "supplyScheduleDays": [
                    "MONDAY",
                    "TUESDAY",
                    "WEDNESDAY",
                    "THURSDAY",
                    "FRIDAY",
                    "SATURDAY",
                    "SUNDAY",
                ],
                "deliveryDurationDays": 1,
            }
        }
    except Exception as e:
        print(e)
        return False
    return testProduct


def updatePrices(prices):
    url = f"https://api.partner.market.yandex.ru/v2/campaigns/{settings.CAMPAIGN_ID}/offer-prices/updates.json"

    headers = {
        "Authorization": settings.OAUTH_YANDEX_MARKET,
        "Content-Type": "application/json",
    }

    r = requests.post(url, data=json.dumps(prices), headers=headers)
    return r.status_code, r.json()


def updateProducts(product):
    url = f"https://api.partner.market.yandex.ru/v2/campaigns/{settings.CAMPAIGN_ID}/offer-mapping-entries/updates.json"

    headers = {"Authorization": OAUTH_YANDEX_MARKET, "Content-Type": "application/json"}

    r = requests.post(url, data=json.dumps(product), headers=headers)
    return r.status_code, r.json()


def createJsonChunks(makeItems):
    method_name = makeItems.__name__

    chunk_size = 50
    if method_name == "makeProduct":
        chunk_size = 100

    gen = chunkGenerator(chunk_size)
    for i, chunk in enumerate(gen):
        products = []
        for product in chunk:
            if not product:
                print("Fucks up in product")
            try:
                products.append(makeItems(product))
            except:
                print("Exception raised in zerro price")
                pass
        logger(
            json.dumps(products, indent=2),
            f"{i}-{method_name}-chunk.json",
            "yandex_market",
        )

        if method_name == "makePrices":
            yield {"offers": products}
        else:
            yield {"offerMappingEntries": products}


def makePrices(product):
    shopSku = product.one_c_id
    price = 0
    price = float(product.product_stock.first().price)
    if not price:
        raise TypeError()
    item = {
        "shopSku": shopSku,
        "price": {
            "currencyId": "RUR",
            "value": price,
            "discountBase": math.ceil(price + price * 0.1),
        },
    }
    return item


def do_all_update_products(production=False):
    chunkGen = createJsonChunks(makeProduct)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk Size is:", len(chunk["offerMappingEntries"]))
        if production:
            status_code, response = updateProducts(chunk)
            all_responses.append(f"{response}")
            print(f"{i} chunk here", response)
        time.sleep(5)
    try:
        send_mail(
            "Товары на маркете обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.FROM_EMAIL_ADMIN,
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
    print(all_responses)


def do_all_update_prices(production=False):
    chunkGen = createJsonChunks(makePrices)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk length is:", len(chunk["offers"]))
        conn = 1
        while conn <= 5:
            if production:
                try:
                    status_code, response = updatePrices(chunk)
                    all_responses.append(f"{response}")
                    print(f"{i} chunk here || Attempt number-{conn}", response)
                    if status_code == 200:
                        break
                    conn += 1
                    time.sleep(65)
                except:
                    print("Attempt #", conn)
                    continue

        time.sleep(65)
    try:
        send_mail(
            "Цены Товаров на маркете обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.FROM_EMAIL_ADMIN,
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except:
        pass
