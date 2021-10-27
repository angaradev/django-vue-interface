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
                    "id": 85,
                    "values": [{"dictionary_value_id": 0, "value": "Angara"}],
                },
                {
                    "complex_id": 0,
                    "id": 9048,
                    "values": [{"dictionary_value_id": 0, "value": "Lamborgini"}],
                },
                {
                    "complex_id": 0,
                    "id": 7236,
                    "values": [{"dictionary_value_id": 0, "value": "1245545"}],
                },
                {
                    "complex_id": 0,
                    "id": 8229,
                    "values": [
                        {"dictionary_value_id": 0, "value": "Крыло автомобильное"}
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 4074,
                    "values": [{"dictionary_value_id": 0, "value": "PFbomAhc51M"}],
                },
                {
                    "complex_id": 0,
                    "id": 4191,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": "Description goes here blah blah blag",
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 7204,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": "RolsRoys",
                        }
                    ],
                },
                {
                    "complex_id": 0,
                    "id": 7212,
                    "values": [
                        {
                            "dictionary_value_id": 0,
                            "value": "Model Auto",
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
            "barcode": "string",
            "category_id": 93446776,
            "color_image": "string",
            "depth": 20,
            "dimension_unit": "cm",
            "height": 20,
            "image_group_id": "string",
            "images": [
                "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2730_LFSeBqR.JPG",
                "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2732_JlZkQ2r.JPG",
                "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2729_7LFeCod.JPG",
                "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2731_RrgXB6q.JPG",
            ],
            "primary_image": "http://localhost:8000/media/parts/1362564080NG/kmk_glass/tmb/IMG_7470_ducato_sIdV3Dl.JPG",
            "name": "Test product from API",
            "offer_id": "1",
            "old_price": "300",
            "premium_price": "200",
            "price": "250",
            "vat": "0",
            "weight": 2,
            "weight_unit": "kg",
            "width": 20,
        }
    ]
}


def get_cat(product):
    "Creating vendor cateory"
    for cat in product.category.all():
        for inn_cat in cat.get_ancestors(include_self=False):
            yc = inn_cat.ozon_category.name
            if yc:
                return yc


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
            brand = "ORIGINAL"
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
        payload = {
            "items": [
                {
                    "category_id": 93446776,
                    "color_image": "string",
                    "depth": 20,
                    "dimension_unit": "cm",
                    "height": 20,
                    "image_group_id": "string",
                    "images": [
                        "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2730_LFSeBqR.JPG",
                        "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2732_JlZkQ2r.JPG",
                        "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2729_7LFeCod.JPG",
                        "https://angara77.ru/media/parts/1336735080/fiat/alfa/lancia/tmb/DSCN2731_RrgXB6q.JPG",
                    ],
                    "primary_image": "http://localhost:8000/media/parts/1362564080NG/kmk_glass/tmb/IMG_7470_ducato_sIdV3Dl.JPG",
                    "name": "Test product from API",
                    "offer_id": "1",
                    "old_price": "300",
                    "premium_price": "200",
                    "price": "250",
                    "vat": "0",
                    "weight": 2,
                    "weight_unit": "kg",
                    "width": 20,
                    "attributes": [
                        {
                            "complex_id": 0,
                            "id": 85,
                            "values": [{"dictionary_value_id": 0, "value": "Angara"}],
                        },
                        {
                            "complex_id": 0,
                            "id": 9048,
                            "values": [
                                {"dictionary_value_id": 0, "value": "Lamborgini"}
                            ],
                        },
                        {
                            "complex_id": 0,
                            "id": 7236,
                            "values": [{"dictionary_value_id": 0, "value": "1245545"}],
                        },
                        {
                            "complex_id": 0,
                            "id": 8229,
                            "values": [
                                {
                                    "dictionary_value_id": 0,
                                    "value": "Крыло автомобильное",
                                }
                            ],
                        },
                        {
                            "complex_id": 0,
                            "id": 4074,
                            "values": [
                                {"dictionary_value_id": 0, "value": "PFbomAhc51M"}
                            ],
                        },
                        {
                            "complex_id": 0,
                            "id": 4191,
                            "values": [
                                {
                                    "dictionary_value_id": 0,
                                    "value": "Description goes here blah blah blag",
                                }
                            ],
                        },
                        {
                            "complex_id": 0,
                            "id": 7204,
                            "values": [
                                {
                                    "dictionary_value_id": 0,
                                    "value": "RolsRoys",
                                }
                            ],
                        },
                        {
                            "complex_id": 0,
                            "id": 7212,
                            "values": [
                                {
                                    "dictionary_value_id": 0,
                                    "value": "Model Auto",
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
            ]
        }
    except Exception as e:
        print(e)
        return False
    return testProduct


"""
Тип товара
Артикул
Бренд
Наименование детали
Вес
Габаритные размеры упаковки
Штрихкод
"""
