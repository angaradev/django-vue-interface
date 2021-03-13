from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from product.models.models import Product, Store


class Price(models.Model):
    """
    Class handling product prices
    """

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"

    def __str__(self):
        return self.product.full_name

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_price"
    )
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)


class PriceHistory(models.Model):
    """
    Class handling product price history
    """

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"

    def __str__(self):
        return self.product.full_name

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_price_history"
    )
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    dollar_rate = models.FloatField()
    price_date = models.DateTimeField(auto_now_add=True)


class Stock(models.Model):
    """
    Handling products on stock
    """

    class Meta:
        verbose_name = "Сток"
        verbose_name_plural = "Стоки"

    def __str__(self):
        return self.product.full_name

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="product_stock"
    )
    store = models.OneToOneField(
        Store, on_delete=models.CASCADE, related_name="store_stock"
    )
    quantity = models.IntegerField()
    availability_days = models.IntegerField()
