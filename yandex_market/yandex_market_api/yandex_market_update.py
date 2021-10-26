import os
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


maslo_lst = [
    24962,
    25508,
    3226,
    25332,
    24684,
    24700,
    16567,
    23850,
    24352,
    16330,
    16683,
    16674,
    23048,
    14569,
    24821,
    24628,
    14567,
    24813,
    24740,
    25469,
    22752,
    22641,
    24644,
    11145,
    24549,
    23714,
    11189,
    23715,
    15768,
    15791,
    24260,
    23318,
    24698,
    15803,
    23853,
    24194,
    3615,
    25305,
    23704,
    24094,
    25486,
    25087,
    25467,
    25489,
    25487,
    23780,
    23781,
    25429,
    25088,
    25482,
    25483,
    25485,
    25484,
    25481,
    24859,
    23463,
    24861,
    24862,
    25453,
    3434,
]


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
    products = (
        Product.objects.filter(product_image__img150__isnull=False)
        .filter(product_stock__quantity__gt=0)
        .exclude(one_c_id__in=maslo_lst)
        .distinct()
    )
    print("Products selected:", products.count())
    for i in range(0, products.count(), n):
        yield products[i : i + n]


def makeProduct(product):
    name = ""
    car_make = ""
    car_model = ""
    imgUrl = "https://angara77.ru"  # settings.SITE_URL
    siteUrl = "https://partshub.ru"  # settings.SITE_URL
    description = "Материлы изготовления: сталь, алюминий, резина, стекло, пластик. Произведена на высокоточном оборудовании, с соблюдением всех допусков."
    try:
        car_make = product.car_model.first().carmake.name.upper()
        car_model = product.car_model.first().name.upper()
    except Exception as e:
        # print("No name in product", product)
        # print(e)
        pass
    try:
        name = f"{product.name.capitalize()} {car_make} {car_model} {product.name2 if product.name2 else ''}".strip()
        pattern = r"(\(.+\))|(\s\w+\/\w+)"
        chk = re.search(pattern, name)
        if chk:
            logger(
                f"{name}, {product.one_c_id} \n", "fucked_products.log", "yandex_market"
            )
        name = re.sub(pattern, "", name)
    except:
        print("Name is fucks up")

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

    try:
        if hasattr(product, "product_description"):
            soup = BeautifulSoup(product.product_description.text, "lxml")
            description = soup.get_text()
            description = re.sub("&nbsp;", " ", description, flags=re.IGNORECASE)
    except Exception as e:
        pass

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
                ],
                "deliveryDurationDays": 1,
            }
        }
    except Exception as e:
        print(e)
        return False
    return testProduct


data = {
    "offers": [
        {
            "marketSku": 101413224188,
            "price": {
                "currencyId": "RUR",
                "value": 6969.00,
                "discountBase": 7500,
                "vat": 5,
            },
        }
    ]
}


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
            "discountBase": price + price * 0.1,
            "vat": 5,
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


def do_all_update_prices():
    chunkGen = createJsonChunks(makePrices)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk length is:", len(chunk["offers"]))
        conn = 1
        while conn <= 5:
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
