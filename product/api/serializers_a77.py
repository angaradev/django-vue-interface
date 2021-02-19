from rest_framework import serializers
from product.models import Category, Product
from rest_framework.reverse import reverse


class CategoriesSerializerfFlat(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    # parent = serializers.SerializerMethodField(read_only=True)

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
