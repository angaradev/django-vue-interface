import os, math, progressbar
from quora.common_lib.logger import logger
import re
import pathlib
from bs4 import BeautifulSoup
from quora.local_settings import OAUTH_OZON, OZON_ID
from product.models import Product
from django.conf import settings
import requests, json, time
from django.core.mail import send_mail
from quora.common_lib.get_parent_category import parent_category
from product.models import CategoryOzon
from quora.common_lib.get_or_make_description import clear_description


def make_product(product):
    def get_cat_two(product):
        cats = product.category.all()
        tmp = []
        for cat in cats:
            for inn_cat in cat.get_ancestors(include_self=True):
                tmp.append(inn_cat.id)
        cts = CategoryOzon.objects.filter(shop_cat__in=tmp)
        ret = max([x.shop_cat.id for x in cts])
        final = cts.get(shop_cat=ret)
        return final.cat_id, final.name, final.ozon_type

    name = ""
    car_make = ""
    car_model = ""
    image_group_id = None
    imgUrl = "https://angara77.ru"  # settings.SITE_URL
    siteUrl = "https://partshub.ru"  # settings.SITE_URL
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
        pass
    #         print("Name is fucks up")

    brand = "original"
    try:

        brand = product.brand.brand.capitalize()
        brand = re.sub(r"[\-\/]", " ", brand)
        if not brand or brand == "оригинал":
            brand = "original"
        if brand.lower() == "mobis".lower():
            brand = "original"
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
    primary_image = ""
    try:
        images = [f"{imgUrl}{x.img800.url}" for x in product.product_image.all()]
        if len(images):
            primary_image = images[0]
    except Exception as e:
        # print(e)
        pass
    # If we dont have category of ozon continue

    try:
        category_id, category_name, ozon_type = get_cat_two(product)
        if category_name:
            category_name = category_name.strip()
    except Exception as e:
        raise ValueError("probably not found category for this product")

    description = clear_description(product)
    payload = None
    image_group_id = product.one_c_id or ""

    price = 0
    old_price = 0
    premium_price = 0
    try:
        premium_price = float(product.product_stock.first().price)
        old_price = math.ceil(premium_price + premium_price * 0.2)
        price = math.ceil(premium_price + premium_price * 0.1)
    except Exception as e:
        pass
    #         print('Shit in price', e)
    cat_number = ""
    try:
        cat_number = product.cat_number or ""
    except:
        pass

    youtube_id = ""
    try:
        youtube_id = product.product_video.first().youtube_id
    except Exception as e:
        pass
    #         print('No Youtube id', e)

    try:
        payload = {
            "category_id": category_id,
            #                     "color_image": "string",
            "depth": 20,
            "dimension_unit": "cm",
            "height": 20,
            "image_group_id": str(image_group_id),
            "images": images,
            "primary_image": primary_image,
            "name": name,
            "offer_id": str(product.one_c_id),
            "old_price": str(old_price),
            "premium_price": str(premium_price),
            "price": str(price),
            "vat": "0",
            "weight": 2,
            "weight_unit": "kg",
            "width": 20,
            "attributes": [
                {
                    "complex_id": 0,
                    "id": 85,
                    "values": [{"dictionary_value_id": 0, "value": brand}],
                },
                {
                    "complex_id": 0,
                    "id": 8205,
                    "values": [{"dictionary_value_id": 0, "value": 1825}],
                },
                {
                    "complex_id": 0,
                    "id": 9048,
                    "values": [{"dictionary_value_id": 0, "value": name}],
                },
                {
                    "complex_id": 0,
                    "id": 7236,
                    "values": [{"dictionary_value_id": 0, "value": cat_number}],
                },
                {
                    "complex_id": 0,
                    "id": 8229,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": ozon_type,
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 4074,
                    "values": [{"dictionary_value_id": 0, "value": youtube_id}],
                },
                {
                    "complex_id": 0,
                    "id": 11254,
                    "values": [{"dictionary_value_id": 0, "value": description}],
                },
                {
                    "complex_id": 0,
                    "id": 4191,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": description,
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 7204,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": car_make,
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 7212,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": car_model,
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 9782,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": "Не опасен",
                        }
                    ],
                },
            ],
        }
    except Exception as e:
        print("Crap happened in main exception", e)
    return payload


def chunkGenerator(chunk_size):
    """
    Creating products by chanks size is given in params
    """
    # Chunk size
    n = chunk_size
    # Select products with images and prices
    products = (
        Product.objects.filter(product_image__img150__isnull=False)
        .filter(product_stock__quantity__gt=0)
        .distinct()
    )
    print("Products selected:", products.count())
    for i in range(0, products.count(), n):
        yield products[i : i + n]


def makeJsonChunks(makeItems):

    method_name = makeItems.__name__
    chunks = chunkGenerator(10)
    success = 0
    fail = 0

    for i, chunk in enumerate(chunks):
        result = []
        for product in chunk:
            try:
                result.append(makeItems(product))
                success += 1
            except Exception as e:
                fail += 1

        logger(
            json.dumps({"items": result}, indent=2),
            f"{i}-{method_name}-chunk.json",
            "ozon",
        )
        yield {"items": result}

    print("Success:", success, "Fail:", fail)


def test():
    res = next(makeJsonChunks(make_product))


def updateProducts(chunk):
    url = f"https://api-seller.ozon.ru/v2/product/import"

    headers = {
        "Client-Id": str(OZON_ID),
        "Api-Key": str(OAUTH_OZON),
        "Content-Type": "application/json",
    }

    r = requests.post(url, data=json.dumps(chunk), headers=headers)
    return r.status_code, r.json()


def do_all_update_products(production=False, iterations=2):
    """
    production=False  -- Pass True for real request to server
    iterations=2 -- if set 0 do till the end
    send request to server but printing results in BASE_DIR/logs/ozon/
    """
    chunkGen = makeJsonChunks(make_product)
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print("Chunk Size is:", len(chunk["items"]))
        if not iterations == 0:
            if i == iterations:
                break
        if production:
            status_code, response = updateProducts(chunk)
            all_responses.append(f"{response}")
            print(f"{i} chunk here", response)
        time.sleep(5)
    try:
        send_mail(
            "Товары на OZONe обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.FROM_EMAIL_ADMIN,
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
    print(all_responses)
