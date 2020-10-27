from rest_framework import serializers
from product.models import (
    Product,
    ProductImage,
    Category,
    Units,
    CarModel,
    CarMake,
    CarEngine,
    Country,
    BrandsDict,
    ProductVideos,
    ProductDescription,
    ProductAttribute,
    ProductAttributeName,
    Cross,
)


class ProductCrossSerializer(serializers.ModelSerializer):
    """
    Serializer for getting product Crosses
    """

    class Meta:
        model = Cross
        fields = ["cross"]
        depth = 0


class RedGetSingleProductSerializer(serializers.ModelSerializer):
    """
    Serializer for getting single product for site no authentication required
    Also getting all related fields like images, videos, attributes, etc...
    """

    product_cross = ProductCrossSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "name2",
            "cat_number",
            "slug",
            "brand",
            "unit",
            "car_model",
            "category",
            "related",
            "engine",
            "product_image",
            "product_video",
            "product_description",
            "product_cross",
            "product_attribute",
            "one_c_id",
        ]
        depth = 0  # Dont change it All may craches
