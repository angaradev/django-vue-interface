from django.db import models
from product.models.models import Category


class CategoryYandexMarket(models.Model):
    shop_cat = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="yandex_category"
    )
    cat_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)


class CategoryOzon(models.Model):
    shop_cat = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="ozon_category"
    )
    cat_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
