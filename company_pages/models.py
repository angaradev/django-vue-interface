from django.db import models
from ckeditor.fields import RichTextField


class CompanyPages(models.Model):

    title = models.CharField(max_length=255)
    textHtml = RichTextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Страницa Компании"
        verbose_name_plural = "Страницы Компании"

    def __str__(self):
        return self.title
