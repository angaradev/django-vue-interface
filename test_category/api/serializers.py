from rest_framework import serializers
from test_category.models import Categories
from rest_framework.reverse import reverse


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoriesSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Categories
        fields = "__all__"


class NoRecursionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ["id", "type", "name", "slug", "image", "layout", "parent", "children"]
        depth = 1


class DepthOneCategorySerializer(serializers.ModelSerializer):
    children = NoRecursionCategorySerializer(many=True)

    class Meta:
        model = Categories
        fields = ["id", "type", "name", "slug", "image", "layout", "parent", "children"]
