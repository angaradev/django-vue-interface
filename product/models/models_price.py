from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from product.models.models import Product, Store


def get_default_store():
    try:
        store = Store.objects.get(id=1)
        return store
    except:
        print("No store in the database")
    return None


class Price(models.Model):
    """
    Class handling product prices
    """

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"

    def __str__(self):
        return self.product.full_name

    value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )


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

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_stock"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="store_stock"
    )
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    quantity = models.IntegerField()
    availability_days = models.IntegerField()

    def __str__(self):
        return self.product.full_name
