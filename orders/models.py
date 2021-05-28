from users.models import AutoUser, CustomUser
from django.db import models
from product.models import Product


class Orders(models.Model):
    class StatusChoices(models.TextChoices):
        ORDERED = ("ORD", "ПОЛУЧЕН")
        INPROGRESS = ("PROG", "СОБИРАЕТСЯ")
        SENT = ("SENT", "ОТПРАВЛЕН")
        DELIVERED = ("DELIV", "ДОСТАВЛЕН")

    date = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50, choices=StatusChoices.choices, default=StatusChoices.ORDERED
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    autouser = models.ForeignKey(AutoUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.number

    @property
    def total(self):
        sum = 0
        try:
            prods = self.order_product.all()
            for prod in prods:
                sum += prod.product_price
        except:
            pass
        print(sum)
        return sum


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name="order_products"
    )
    product_id = models.IntegerField()
    product_price = models.DecimalField(max_digits=14, decimal_places=2)
    product_name = models.CharField(max_length=555)
    product_car = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255)
    qty = models.IntegerField()

    class Meta:
        verbose_name = "Детали заказа"
        verbose_name_plural = "Детали заказа"

    def __str__(self):
        return self.product_name
