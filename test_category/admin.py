from django.contrib import admin

from .models import Categories, Brands, Product

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Brands)
