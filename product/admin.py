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



#admin.site.register(Category, MPTTModelAdmin)

from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
    

class CategoryAdmin(DjangoMpttAdmin):
    tree_auto_open = 0
    tree_load_on_demand = 0
    use_context_menu = True

admin.site.register(Category, CategoryAdmin)
