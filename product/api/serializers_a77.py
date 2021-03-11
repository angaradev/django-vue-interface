from rest_framework import serializers
from product.models import Category, Product
from rest_framework.reverse import reverse


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
