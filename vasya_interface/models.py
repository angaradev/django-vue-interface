from django.db import models


class Rows(models.Model):
    uuid = models.CharField(max_length=255)
    oneCId = models.IntegerField()
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=20)
    catNumber = models.CharField(max_length=20)
    description = models.TextField()
    isDone = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Карточки в Работе"

    def __str__(self):
        return self.name
