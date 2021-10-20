from quora.local_settings import OAUTH_YANDEX_MARKET
from product.models import Product
from django.conf import settings
import requests, json, time


maslo_lst = [59696, 949434]


def chunkGenerator():
    # Chunk size
    n = 490
    # Select products with images and prices
    products = (
        Product.objects.filter(product_image__img150__isnull=False)
        .filter(product_stock__quantity__gt=0)
        .exclude(one_c_id__in=maslo_lst)
        .distinct()
    )
    for i in range(0, products.count(), n):
        yield products[i : i + n]


def makeProduct(product):
    name = f"{product.name.capitalize()} \
        {product.car_model.first().carmake.name.upper()} \
        {product.car_model.first().name.upper()} \
        {product.name2 if product.name2 else ''}".strip()
    brand = product.brand.brand.upper()

    country = [product.brand.country.upper() if product.brand.country else ""]
    images = []
    try:
        imgUrl = settings.SITE_URL
        images = [f"{imgUrl}{x.img800.url}" for x in product.product_image.all()]
    except Exception as e:
        print(e)
    category = ""
    try:
        category = product.category.first().name.upper()
    except Exception as e:
        print(e)

    testProduct = {
        "offer": {
            "shopSku": product.one_c_id,
            "name": name,
            "category": category,
            "manufacturer": brand,
            "manufacturerCountries": country,
            "weightDimensions": {
                "length": 15.0,
                "width": 24.0,
                "height": 12.5,
                "weight": 3.1,
            },
            "urls": [f"https://partshub.ru/product/{product.slug}"],
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
    url = "https://api.partner.market.yandex.ru/v2/campaigns/22527279/offer-prices/updates.json"

    headers = {"Authorization": OAUTH_YANDEX_MARKET, "Content-Type": "application/json"}

    r = requests.post(url, data=json.dumps(product), headers=headers)
    return f"{r.json()} {r.status_code}"


def createJsonChunks():
    products = []
    gen = chunkGenerator()

    for chunk in gen:
        for i, product in enumerate(chunk):
            products.append(makeProduct(product))
            if i > 2:
                break
        yield {"offerMappingEntries": products}
        time.sleep(5)


def do_all_update_products():
    chunkGen = createJsonChunks()
    for chunk in chunkGen:
        response = updateProducts(chunk)
        time.sleep(5)
        print(response)
