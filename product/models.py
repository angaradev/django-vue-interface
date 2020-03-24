# -*- coding: utf-8 -*-

import os
from brands.models import BrandsDict
from product.utils import unique_slug_generator, get_youtube_id
from django.db.models.signals import pre_save
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
import io
from django.db.models.signals import post_delete
from django.dispatch import receiver
from PIL import Image, ImageOps
from .utils import delete_file
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True, on_delete=models.CASCADE)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'Категории'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name


# class Category(models.Model):  # Categories of products class
#     name = models.CharField(max_length=100)
#     parent = models.ForeignKey(
#         'self', on_delete=models.CASCADE, blank=True, null=True)
#     slug = models.SlugField(max_length=50)

#     def __str__(self):
#         return self.name


class Units(models.Model):  # Units for parts
    unit_name = models.CharField(max_length=10, default='шт')
    
    class Meta:
        verbose_name = ("Еденица измерения")
        verbose_name_plural = ("Еденицы измерения")

    def __str__(self):
        return self.unit_name


# Class Country
class Country(models.Model):
    country = models.CharField(max_length=45)

    class Meta:
        verbose_name = ("Страна")
        verbose_name_plural = ("Страны")

    def __str__(self):
        return self.country


# Car Make class
class CarMake(models.Model):
    name = models.CharField(max_length=45)
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        verbose_name = ("Марка Машины")
        verbose_name_plural = ("Марки Машин")

    def __str__(self):
        return self.name


class CarEngine(models.Model):
    name = models.CharField(max_length=45, blank=True)

    class Meta:
        verbose_name = ("Двигатель")
        verbose_name_plural = ("Двигатели")

    def __str__(self):
        return self.name

# Car Model class


class CarModel(models.Model):
    name = models.CharField(max_length=45, blank=True)
    engine = models.ManyToManyField(
        CarEngine, blank=True, related_name='car_engine')
    carmake = models.ForeignKey(CarMake, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = ("Модель Машины")
        verbose_name_plural = ("Модели Машины")

    def __str__(self):
        return self.name


# Custom path to upload images
def img_path(instance, filename, *args, **kwargs):
    path = os.path.join(
        str(instance.product.cat_number), str(instance.product.brand).replace(' ', '_'), filename)
    return path


def img_path_tmb(instance, filename, *args, **kwargs):
    path = os.path.join(
        str(instance.product.cat_number), str(instance.product.brand).replace(' ', '_'), 'tmb', filename)
    return path


###############################################################################
# Product images
class ProductImage(models.Model):
    image = models.ImageField(
        max_length=255, upload_to=img_path, null=True, blank=True)
    img150 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img245 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img500 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img800 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True, related_name='product_image')
    class Meta:
        verbose_name = ("Фото")
        verbose_name_plural = ("Фото")

    def save(self, *args, **kwargs):

        size = (150, 245, 500, 800, 1200)
        method = Image.ANTIALIAS

        im = Image.open(io.BytesIO(self.image.read()))
        #im = Image.open(self.image)
        imw, imh = im.size
        if imw > size[4]:
            img_big = ImageOps.fit(im, (size[4], size[4]), method=method,
                                   bleed=0.0, centering=(0.5, 0.5))
            output = io.BytesIO()
            img_big.save(output, format='JPEG', quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output, 'ImageField', f'{self.image.name}', 'image/jpeg', output.getbuffer().nbytes, 'utf-8', None)

        img150 = ImageOps.fit(im, (size[0], size[0]), method=method,
                              bleed=0.0, centering=(0.5, 0.5))
        output = io.BytesIO()
        img150.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.img150 = InMemoryUploadedFile(
            output, 'ImageField', f'{self.image.name}', 'image/jpeg', output.getbuffer().nbytes, 'utf-8', None)

        img245 = ImageOps.fit(im, (size[1], size[1]), method=method,
                              bleed=0.0, centering=(0.5, 0.5))
        output = io.BytesIO()
        img245.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.img245 = InMemoryUploadedFile(
            output, 'ImageField', f'{self.image.name}', 'image/jpeg', output.getbuffer().nbytes, 'utf-8', None)

        img500 = ImageOps.fit(im, (size[2], size[2]), method=method,
                              bleed=0.0, centering=(0.5, 0.5))
        output = io.BytesIO()
        img500.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.img500 = InMemoryUploadedFile(
            output, 'ImageField', f'{self.image.name}', 'image/jpeg', output.getbuffer().nbytes, 'utf-8', None)

        img800 = ImageOps.fit(im, (size[3], size[3]), method=method,
                              bleed=0.0, centering=(0.5, 0.5))
        output = io.BytesIO()
        img800.save(output, format='JPEG', quality=90)
        output.seek(0)

        self.img800 = InMemoryUploadedFile(
            output, 'ImageField', f'{self.image.name}', 'image/jpeg', output.getbuffer().nbytes, 'utf-8', None)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product.slug) + '_' + str(self.id)

###############################################################################


# Product Videos
class ProductVideos(models.Model):
    youtube_id = models.CharField(max_length=45, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Видео")
        verbose_name_plural = ("Видео")

# Product Description


class ProductDescription(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Описание товара")
        verbose_name_plural = ("Описания товара")


class Product(models.Model):  # Main table product
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(BrandsDict, on_delete=models.DO_NOTHING,
                              null=True, blank=True, related_name='product_brand')
    car_model = models.ForeignKey(
        CarModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_number = models.CharField(max_length=255)
    category = models.ManyToManyField(
        Category, related_name='category_reverse')
    # Field for the cross selling products many many
    related = models.ManyToManyField('self', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, blank=True)
    one_c_id = models.IntegerField(unique=True, blank=True, null=True)
    unit = models.ForeignKey(
        'Units', on_delete=models.DO_NOTHING, related_name='product_unit')
    active = models.BooleanField(default=True)
    engine = models.ForeignKey(
        'CarEngine', on_delete=models.DO_NOTHING, blank=True)
    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")

    def __str__(self):
        return self.name

# Crosses parts


class Cross(models.Model):
    cross = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Кросс")
        verbose_name_plural = ("Кроссы")

    def __str__(self):
        return self.product


# Product Attribute
class ProductAttribute(models.Model):
    attribute_name = models.CharField(max_length=45, null=True)
    attribute_value = models.CharField(max_length=45, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        verbose_name = ("Атрибут")
        verbose_name_plural = ("Атрибуты")

################### Slug pre save receiver ####################################


def slug_save(sender, instance, *args, **kwargs):  # Slug saver
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, instance.name, instance.slug)


pre_save.connect(slug_save, Product)

#################### Youtube ID Pre Save Receiver #############################


def youtube_id_save(sender, instance, *args, **kwargs):  # youtube id saver
    instance.youtube_id = get_youtube_id(instance.url)


pre_save.connect(youtube_id_save, ProductVideos)

#################### File Delete Post Delete Receiver #########################


def delete_files(sender, instance, *args, **kwargs):
    if instance.image:
        delete_file(instance.image.path)
    if instance.img150:
        delete_file(instance.img150.path)
    if instance.img245:
        delete_file(instance.img245.path)
    if instance.img500:
        delete_file(instance.img500.path)
    if instance.img800:
        delete_file(instance.img800.path)


post_delete.connect(delete_files, ProductImage)
