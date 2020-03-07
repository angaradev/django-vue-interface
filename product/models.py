from django.db import models
from brands.models import BrandsDict


# Units for parts
class Units(models.Model):
    unit = models.CharField(max_length=10)



# Main table product
class Product(models.Model):
    brand = models.OneToOneField(BrandsDict, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    related = models.ManyToManyField('self') # Field for the cross selling products many many
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    unit = models.OneToOneField(Units, on_delete=models.DO_NOTHING)



    
# Categories of products class
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50)

# Class Country
class Country(models.Model):
    country = models.CharField(max_length=45)


# Car Make class
class CarMake(models.Model):
    name = models.CharField(max_length=45)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)


# Car Model class 
class CarModel(models.Model):
    name = models.CharField(max_length=45)
    engine = models.CharField(max_length=45) 
    carmake = models.ForeignKey(CarMake, on_delete=models.DO_NOTHING)





# Crosses parts
class Cross(models.Model):
    cross = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)




# Cross Sale parts and Related for the site
class Tags(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)




# Product images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    


# Thumbnails for images
class ProductThumb(models.Model):
    pass


# Product Videos
class ProductVideos(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

# Product Description
class ProductDescription(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


# Product Attribute
class ProductAttribute(models.Model):
    product = models.ManyToManyField(Product)# Relation to product Model
    attribute = models.CharField(max_length=45, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)




