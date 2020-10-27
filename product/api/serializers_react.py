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


class AttributesNameSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()

    class Meta:
        model = ProductAttributeName
        fields = ["name"]


class AttributesSerializer(serializers.ModelSerializer):

    attribute_name = AttributesNameSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ["attribute_name", "attribute_value"]


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ["product", "created_date", "updated_date"]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "lft", "rght", "tree_id", "level", "parent"]


class RedGetSingleProductSerializer(serializers.ModelSerializer):
    """
    Serializer for getting single product for site no authentication required
    Also getting all related fields like images, videos, attributes, etc...
    """

    product_cross = ProductCrossSerializer(many=True, read_only=True)
    attributes = AttributesSerializer(many=True, read_only=True)
    images = ProductImagesSerializer(many=True, read_only=True)
    categories = CategoriesSerializer(many=True, read_only=True, source="category")

    class Meta:
        model = Product
        fields = [
            "categories",
            "id",
            "name",
            "name2",
            "excerpt",
            "description",
            "slug",
            "sku",
            "partNumber",
            "stock",
            "price",
            "compareAtPrice",
            "images",
            "badges",
            "rating",
            "reviews",
            "availability",
            "compatibility",
            "brand",
            # type
            "attributes",
            "tags",
            "unit",
            "car_model",
            "related",
            "engine",
            "product_video",
            "product_cross",
        ]
        depth = 1  # Dont change it All may craches
