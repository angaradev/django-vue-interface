from django.db import models
from product.models import Category
from django.conf import settings
from ckeditor.fields import RichTextField
from product.models import Category
from transliterate import translit
from django.utils.text import slugify


class Categories(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категоиря Блога"
        verbose_name_plural = "Категории Блога"

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=255)
    text = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to=settings.BLOG_IMAGES)
    parts_category = models.ManyToManyField(Category, related_name="parts_categories")
    categories = models.ManyToManyField("Categories", related_name="blog_categories")
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default=settings.DEFAULT_AUTHOR)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title, "ru", reversed=True))
        super().save(*args, **kwargs)


# id: 2,
#     title: 'Logic Is The Study Of Reasoning And Argument Part 2',
#     image: '/images/posts/post-2.jpg',
#     categories: ['Latest News'],
#     date: '2019-09-05',
