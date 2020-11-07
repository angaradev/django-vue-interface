from django.db import models
from users.models import CustomUser


class Makes(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Марка"

    def __str__(self):
        return self.name


class Years(models.Model):
    year = models.IntegerField()

    class Meta:
        verbose_name = "Год"

    def __str__(self):
        return f"{self.year}"


class Vehicle(models.Model):

    year_from = models.ForeignKey(
        Years, on_delete=models.DO_NOTHING, related_name="year_from"
    )
    year_to = models.ForeignKey(
        Years, on_delete=models.DO_NOTHING, related_name="year_to"
    )
    make = models.ForeignKey(Makes, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=255)
    engine = models.ForeignKey("Engine", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Автомобил"
        verbose_name_plural = "Автомобили"

    @property
    def year(self):
        return [int(self.year_from.year), int(self.year_to.year)]

    def __str__(self):
        return self.model


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Engine(models.Model):

    FUELS = (("D", "Desel"), ("G", "Gasoline"))
    VOLUMES = (
        ("3", "3.0"),
        ("3.5", "3.5"),
        ("2.5", "2.5"),
        ("2", "2.0"),
        ("1.5", "1.5"),
    )

    name = models.CharField(max_length=100)
    fuel = models.CharField(max_length=10, choices=FUELS, default="D")
    volume = models.CharField(max_length=10, choices=VOLUMES, default="2.5")

    class Meta:
        verbose_name = "Двигатель"

    def __str__(self):
        return self.name


class UserVehicles(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    vehicles = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="vehicles"
    )

    class Meta:
        verbose_name = "Машина Пользователя"
        verbose_name_plural = "Машины пользователя"


##
