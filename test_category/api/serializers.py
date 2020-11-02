from rest_framework import serializers
from test_category.models import Categories
from rest_framework.reverse import reverse


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ParentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Categories
        fields = [
            "id",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
        depth = 3


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer for make categories working well
    it is making right fields for frontend
    it is solved big problem by the way
    """

    children = RecursiveField(many=True)
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = Categories
        fields = [
            "id",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
        depth = 3


# class NoRecursionCategorySerializer(serializers.ModelSerializer):
#     parent = ParentSerializer()

#     class Meta:

#         model = Categories
#         fields = [
#             "id",
#             "type",
#             "name",
#             "slug",
#             "image",
#             "layout",
#             "parent",
#             "children",
#         ]
#         depth = 2


# class DepthOneCategorySerializer(serializers.ModelSerializer):
#     children = NoRecursionCategorySerializer(many=True)

#     class Meta:
#         model = Categories
#         fields = ["id", "type", "name", "slug", "image", "layout", "parent", "children"]
