from django.db import models


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
    total = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.number
