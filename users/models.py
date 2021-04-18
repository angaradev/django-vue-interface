from django.db import models


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class AutoUser(models.Model):
    userId = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
