import os
import re
import pathlib
from quora.local_settings import OAUTH_YANDEX_MARKET
from product.models import Product
from django.conf import settings
import requests, json, time
from django.core.mail import send_mail


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


def logging(string, filename):
    path = os.path.join(settings.BASE_DIR, "logs")
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    final_path = os.path.join(path, filename)

    with open(os.path.join(path, filename), "a") as file:
        file.write(string)


def chunkGenerator():
    # Chunk size
    n = 200
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
            logging(f"{name}, {product.one_c_id} \n", "fucked_products.log")
            # with open(f"/home/manhee/tmp/chunks/fucked_prods.txt", "a") as file:
            #     file.write(f"{name}, {product.one_c_id} \n")
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

    country = "Корея"
    try:
        country = product.brand.country.upper() if product.brand.country else ""
    except Exception as e:
        # print("No counnreis found")
        pass
    images = []
    try:
        images = [f"{imgUrl}{x.img800.url}" for x in product.product_image.all()]
    except Exception as e:
        # print(e)
        pass
    category = ""
    try:
        category = product.category.first().name.upper()
    except Exception as e:
        # print(e)
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


def sendRequest():
    url = "https://api.partner.market.yandex.ru/v2/campaigns/22527279/offer-prices/updates.json"

    headers = {
        "Authorization": settings.OAUTH_YANDEX_MARKET,
        "Content-Type": "application/json",
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json(), r.status_code)


def updateProducts(product):
    url = "https://api.partner.market.yandex.ru/v2/campaigns/22527279/offer-mapping-entries/updates.json"

    headers = {"Authorization": OAUTH_YANDEX_MARKET, "Content-Type": "application/json"}

    r = requests.post(url, data=json.dumps(product), headers=headers)
    return f"{r.json()} {r.status_code}"


def createJsonChunks():
    gen = chunkGenerator()

    for i, chunk in enumerate(gen):
        products = []
        for product in chunk:
            if not product:
                print("Fucks up in product")
            products.append(makeProduct(product))
        # with open(f"/home/manhee/tmp/chunks/{i}-chunk.json", "w") as file:
        #     file.write(json.dumps(products, indent=2))

        yield {"offerMappingEntries": products}


def do_all_update_products():
    chunkGen = createJsonChunks()
    all_responses = []
    for i, chunk in enumerate(chunkGen):
        print(len(chunk["offerMappingEntries"]))
        response = updateProducts(chunk)
        all_responses.append(response)
        print(f"{i} chunk here", response)
        time.sleep(2)
    try:
        send_mail(
            "Товары на маркете обновились",
            f"Скрипт, angara77.ru django/products/syncronizators/yandex_market_update.py который обновляет или добавляет товары обновился статус коды\
            и количество чанков {json.dumps(all_responses)}",
            settings.COMPANY_INFO["email"],
            settings.EMAIL_ADMINS,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
    print(all_responses)
