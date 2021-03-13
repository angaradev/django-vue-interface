from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from product.models.models import Product


class Price(models.Model):
    """
    Class handling product prices
    """

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_price"
    )
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)


class PriceHistory(models.Model):
    """
    Class handling product price history
    """

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_price_history"
    )
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    dollar_rate = models.FloatField()
    price_date = models.DateTimeField(auto_now_add=True)


class Store(models.Model):
    """
    Class for handling stores
    """

    name = models.CharField(max_length=255)
    location_city = models.CharField(max_length=50)
    location_address = models.CharField(max_length=100)


class Stock(models.Model):
    """
    Handling products on stock
    """

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_stock"
    )
    store = models.OneToOneField(
        Store, on_delete=models.CASCADE, related_name="store_stock"
    )
