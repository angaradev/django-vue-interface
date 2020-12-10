from rest_framework import serializers
from .models import Rows


class RowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = "__all__"


class CheckProductSerializer(serializers.Serializer):
    one_c_id = serializers.IntegerField(read_only=True)
    has_description = serializers.BooleanField(required=False)
    have_photo = serializers.BooleanField(required=False)
    have_attribute = serializers.BooleanField(required=False)
    have_description = serializers.BooleanField(required=False)
    have_video = serializers.BooleanField(required=False)
