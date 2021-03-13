from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from product.models.models import Product


class Price(models.Model):
    """
    Class handling product prices
    """

    pass


class PriceHistory(models.Model):
    """
    Class handling product price history
    """

    pass


class Stock(models.Model):
    """
    Handling products on stock
    """

    pass


class Stores(models.Model):
    """
    Class for handling stores
    """
