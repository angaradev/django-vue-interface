from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_resized import ResizedImageField


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    image = ResizedImageField(
        size=[100, 100],
        quality=75,
        crop=["middle", "center"],
        upload_to=settings.USER_IMAGES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.email


class AutoUser(models.Model):
    userId = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Автопользователь"
        verbose_name_plural = "Автопользователи"

    def __str__(self):
        return self.userId
