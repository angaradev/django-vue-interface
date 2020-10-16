from django.db import models
from product.models import Category
from django.conf import settings


class Categories(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=settings.BLOG_IMAGES)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категоиря Блога'
        verbose_name_plural = 'Категории Блога'


class Post(models.Model):

    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to=settings.BLOG_IMAGES)
    categories = models.ManyToManyField(
        'Categories', related_name='blog_categories')
    date = models.DateField(auto_now_add=True)
    parts_category = models.ManyToManyField(
        Category, related_name='parts_categories')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

# id: 2,
#     title: 'Logic Is The Study Of Reasoning And Argument Part 2',
#     image: '/images/posts/post-2.jpg',
#     categories: ['Latest News'],
#     date: '2019-09-05',
