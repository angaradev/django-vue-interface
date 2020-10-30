from rest_framework import serializers
from .serializers import CategoriesSerializer
from test_category.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for getting single product for site no authentication required
    Also getting all related fields like images, videos, attributes, etc...
    """

    # attributes = AttributesSerializer(many=True, read_only=True)
    # images = ProductImagesSerializer(many=True, read_only=True)
    categories = CategoriesSerializer(many=True, read_only=True)  # , source="category")

    class Meta:
        model = Product
        fields = [
            "images",
            "id",
            "name",
            "excerpt",
            "description",
            "slug",
            "sku",
            "partNumber",
            "stock",
            "price",
            "compareAtPrice",
            "badges",
            "rating",
            "reviews",
            "availability",
            "compatibility",
            "brand",
            "type",
            "attributes",
            "options",
            "tags",
            "categories",
        ]
        depth = 0  # Dont change it All may craches
