from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from .models import Product, Units, Country, Category, CarMake, CarModel, CarEngine
from .models import (ProductVideos,
                     ProductImage, ProductAttribute, ProductDescription)

admin.site.register(Product)
admin.site.register(Units)
admin.site.register(Country)
admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(CarEngine)
admin.site.register(ProductAttribute)
admin.site.register(ProductDescription)
admin.site.register(ProductImage)
admin.site.register(ProductVideos)



admin.site.register(Category, MPTTModelAdmin)
