from django.db import models


class Makes(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Марка"

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    year = models.ArrayField(IntegerField())
    make = models.ForeignKey(Makes, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=255)
    engine = CharField(max_length=255)

    class Meta:
        verbose_name = "Автомобили"

    def __str__(self):
        return self.model


class Country(models.Model):
    name = models.CharField(max_lenght=50)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Страна"

    def __str__(self):
        return self.name


class Engine(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Двигатель"

    def __str__(self):
        return self.name
