from django.db import models
from ckeditor.fields import RichTextField
from transliterate import translit
from django.utils.text import slugify


class CompanyPages(models.Model):

    title = models.CharField(max_length=255)

    textHtml = RichTextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Страницa Компании"
        verbose_name_plural = "Страницы Компании"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title))
        super().save(*args, **kwargs)
