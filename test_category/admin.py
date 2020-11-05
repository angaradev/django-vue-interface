from django.contrib import admin

from .models import Categories, Brands, Product
from .vehicle_models import Vehicle, Years, Makes, Country, Engine

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Brands)


admin.site.register(Vehicle)
admin.site.register(Years)
admin.site.register(Makes)
admin.site.register(Country)
admin.site.register(Engine)
