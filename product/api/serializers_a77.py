from rest_framework import serializers
from product.models import Category, Product, ProductImage, CarModel
from rest_framework.reverse import reverse
from django.db.models import Q
from django.conf import settings


class CategoriesSerializerfFlat(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    parent = serializers.SerializerMethodField("get_parent", read_only=True)

    def get_parent(self, obj):
        if obj.parent.id == 1:
            return None
        print(obj.parent.id)
        return Category.objects.get(id=obj.parent.id)

    class Meta:
        model = Category
        fields = [
            "id",
            "count",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
        ]
        depth = 3


#################################################################
# Serializers for single product get by slug######
#################################################################


class ProductA77ImageSerializer(serializers.ModelSerializer):
    """Trying to make fill url"""

    img150 = serializers.SerializerMethodField()
    img245 = serializers.SerializerMethodField()
    img800 = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_img150(self, object):
        return settings.SITE_URL + object.img150.url

    def get_img245(self, object):
        return settings.SITE_URL + object.img245.url

    def get_img800(self, object):
        return settings.SITE_URL + object.img800.url

    def get_image(self, object):
        return settings.SITE_URL + object.image.url

    class Meta:
        model = ProductImage
        fields = ("img150", "img245", "img800", "image")


class CarModelA77Serializer(serializers.ModelSerializer):
    """Class for getting some fields from car model and eluminate some big long text html fields"""

    make = serializers.SerializerMethodField()
    make_slug = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, object):
        return settings.SITE_URL + object.image.url if object.image else None

    def get_make(self, object):
        return object.carmake.name

    def get_make_slug(self, object):
        return object.carmake.slug

    class Meta:
        model = CarModel
        fields = ("id", "name", "rusname", "slug", "image", "make", "make_slug")


class AnalogProductA77Serializer(serializers.ModelSerializer):
    """
    Serialzier for getting analog and related products
    """

    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_price(self, object):
        price = 0
        if len(object.product_stock.all()):
            price = object.product_stock.first().price
        return price

    def get_images(self, object):
        imgs = object.product_image.all()
        return ProductA77ImageSerializer(imgs, many=True).data

    class Meta:
        model = Product
        fields = [
            "slug",
            "price",
            "images",
            "name",
            "name2",
            "cat_number",
            "brand",
            "car_model",
            "one_c_id",
        ]
        depth = 1

    car_model = serializers.SerializerMethodField()

    def get_car_model(self, object):
        car_models = object.car_model.all()
        return CarModelA77Serializer(car_models, many=True).data


class ProductA77SerializerBase(serializers.ModelSerializer):
    """
    Serialzier for a77 api get product by slug REST


    """

    model = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    tmb = serializers.SerializerMethodField()

    def get_tmb(self, object):
        tmb = None
        try:
            img = object.product_image.first()
            tmb = settings.SITE_URL + img.img150.url
        except:
            tmb = None
        return tmb

    def get_product_image(self, object):
        imgs = object.product_image.all()
        return ProductA77ImageSerializer(imgs, many=True).data

    def get_price(self, object):
        price = 0
        if len(object.product_stock.all()):
            price = object.product_stock.first().price
        return price

    def get_model(self, object):
        models = object.car_model.all()
        return CarModelA77Serializer(models, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "tmb",
            "product_description",
            "product_image",
            "model",
            "name2",
            "product_video",
            "cat_number",
            "oem_number",
            "category",
            "slug",
            "brand",
            "one_c_id",
            "active",
            "engine",
            "product_cross",
            "product_attribute",
            "product_cross",
        ]
        depth = 1


class ProductA77Serializer(serializers.ModelSerializer):
    """
    Serialzier for a77 api get product by slug REST


    """

    related = serializers.SerializerMethodField()
    analogs = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    tmb = serializers.SerializerMethodField()

    def get_tmb(self, object):
        tmb = None
        try:
            img = object.product_image.first()
            tmb = settings.SITE_URL + img.img150.url
        except:
            tmb = None
        return tmb

    def get_product_image(self, object):
        imgs = object.product_image.all()
        return ProductA77ImageSerializer(imgs, many=True).data

    def get_price(self, object):
        price = 0
        if len(object.product_stock.all()):
            price = object.product_stock.first().price
        return price

    def get_model(self, object):
        models = object.car_model.all()
        return CarModelA77Serializer(models, many=True).data

    def get_analogs(self, object):
        qs = Product.objects.filter(
            Q(cat_number=object.cat_number) | Q(oem_number=object.cat_number)
        )
        return AnalogProductA77Serializer(qs, many=True).data

    def get_related(self, object):
        pattern = object.name.split()
        car_model = object.car_model.first()

        qs = Product.objects.filter(car_model=car_model).filter(
            Q(name__icontains=pattern[0]) | Q(name__icontains=pattern[0])
        )
        return AnalogProductA77Serializer(qs, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "tmb",
            "product_description",
            "product_image",
            "model",
            "name2",
            "product_video",
            "cat_number",
            "oem_number",
            "category",
            "slug",
            "brand",
            "one_c_id",
            "active",
            "engine",
            "product_cross",
            "product_attribute",
            "related",
            "analogs",
            "product_cross",
        ]
        depth = 1


class BlogA77Serializer(serializers.ModelSerializer):
    """
    Serialization for blog but fuck me it is not from here but from local db!!!
    """
