import os
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

payload = {
    "items": [
        {
            "attributes": [
                {
                    "complex_id": 0,
                    "id": 0,
                    "values": [{"dictionary_value_id": 0, "value": "string"}],
                }
            ],
            "barcode": "string",
            "category_id": 0,
            "color_image": "string",
            "complex_attributes": [
                {
                    "attributes": [
                        {
                            "complex_id": 0,
                            "id": 0,
                            "values": [{"dictionary_value_id": 0, "value": "string"}],
                        }
                    ]
                }
            ],
            "depth": 0,
            "dimension_unit": "string",
            "height": 0,
            "image_group_id": "string",
            "images": ["string"],
            "primary_image": "string",
            "images360": ["string"],
            "name": "string",
            "offer_id": "string",
            "old_price": "string",
            "pdf_list": [{"index": 0, "name": "string", "src_url": "string"}],
            "premium_price": "string",
            "price": "string",
            "vat": "string",
            "weight": 0,
            "weight_unit": "string",
            "width": 0,
        }
    ]
}


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
                    "SUNDAY",
                ],
                "deliveryDurationDays": 1,
            }
        }
    except Exception as e:
        print(e)
        return False
    return testProduct
