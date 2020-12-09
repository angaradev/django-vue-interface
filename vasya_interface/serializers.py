from rest_framework import serializers
from .models import Rows


class RowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rows
        fields = "__all__"
