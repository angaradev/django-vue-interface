import os
from brands.models import BrandsDict
from django.db import models
from django.conf import settings


# Units for parts
class Units(models.Model):
    unit = models.CharField(max_length=10, default='шт')

    def __str__(self):
        return self.unit


# Class Country
class Country(models.Model):
    country = models.CharField(max_length=45)

    def __str__(self):
        return self.country


# Car Make class
class CarMake(models.Model):
    name = models.CharField(max_length=45)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class CarEngine(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

# Car Model class


class CarModel(models.Model):
    name = models.CharField(max_length=45)
    engine = models.ForeignKey(
        CarEngine, on_delete=models.CASCADE, null=True, blank=True)
    carmake = models.ForeignKey(CarMake, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


# Categories of products class


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


# Custom path to upload images
def img_path(instance, filename):
    path = os.path.join(
        str(instance.product.cat_number), str(instance.product.brand).replace(' ', '_'), filename)
    return path


# Product images
class ProductImage(models.Model):
    image = models.ImageField(
        max_length=255, upload_to=img_path, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True, related_name='product_image')

    def __str__(self):
        return str(self.product.slug) + '_' + str(self.id)


# Thumbnails for images
#Need to create function for resizing images and save it for different
#sizes
class ProductThumb(models.Model):
    img150 = models.ImageField(
        max_length=255, upload_to='dummy', null=True, blank=True
    )
    img245 = models.ImageField(
        max_length=255, upload_to='dummy', null=True, blank=True
    )
    img500 = models.ImageField(
        max_length=255, upload_to='dummy', null=True, blank=True
    )
    img800 = models.ImageField(
        max_length=255, upload_to='dummy', null=True, blank=True
    )
    image = models.OneToOneField('ProductImage',on_delete=models.CASCADE)


# Product Videos
class ProductVideos(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)

# Product Description


class ProductDescription(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, blank=True, null=True)


class Product(models.Model):  # Main table product
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(BrandsDict, on_delete=models.DO_NOTHING, null=True, blank=True)
    car_model = models.ForeignKey(
        CarModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    cat_number = models.CharField(max_length=255)
    category = models.ManyToManyField(
        Category, related_name='category_reverse')
    # Field for the cross selling products many many
    related = models.ManyToManyField('self', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    unit = models.ForeignKey(
        Units, on_delete=models.DO_NOTHING, blank=True, null=True)
    slug = models.SlugField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

# Crosses parts


class Cross(models.Model):
    cross = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

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
