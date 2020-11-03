from rest_framework import serializers
from test_category.models import Categories, Product
from rest_framework.reverse import reverse


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ParentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = [
            "id",
            "count",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
        depth = 5


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer for make categories working well
    it is making right fields for frontend
    it is solved big problem by the way
    """

    children = RecursiveField(many=True)
    parent = ParentSerializer(read_only=True, many=True)
    count = serializers.IntegerField(read_only=True)
    # count_ser = serializers.SerializerMethodField("get_count_ser", read_only=True)

    # def get_count_ser(self, obj):
    #     return obj.count

    class Meta:
        model = Categories
        fields = [
            "id",
            "count",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
        depth = 3


class NoRecursionCategorySerializer(serializers.ModelSerializer):
    parent = ParentSerializer()
    count = serializers.IntegerField(read_only=True)

    class Meta:

        model = Categories
        fields = [
            "id",
            "count",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
        depth = 2


class DepthOneCategorySerializer(serializers.ModelSerializer):
    children = NoRecursionCategorySerializer(many=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Categories
        fields = [
            "id",
            "count",
            "type",
            "name",
            "slug",
            "image",
            "layout",
            "parent",
            "children",
        ]
