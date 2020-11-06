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

    year = serializers.ListField()
    make = serializers.SerializerMethodField()
    engine = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ["id", "year", "make", "model", "engine"]

    def get_make(self, obj):
        return obj.make.name

    def get_engine(self, obj):
        return obj.engine.name
