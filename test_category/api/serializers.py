from rest_framework import serializers
from test_category.models import Categories


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoriesSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Categories
        fields = "__all__"
