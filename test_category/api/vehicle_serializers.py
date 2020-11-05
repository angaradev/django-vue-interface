from rest_framework import serializers
from test_category.models import Vehicle, Years, Makes


class YearsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Years
        fields = "__all__"


class MakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Makes
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
