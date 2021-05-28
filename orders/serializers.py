from rest_framework import serializers
from .models import OrderProducts, Orders


class OrderProductsSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)

    class Meta:
        model = OrderProducts
        fields = ["product_name", "product_price", "order"]


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductsSerializer(many=True)

    class Meta:
        model = Orders
        fields = [
            "id",
            "date",
            "number",
            "status",
            "user",
            "total",
            "autouser",
            "order_products",
        ]

    def create(self, validated_data):
        import pdb

        pdb.set_trace()
        products_data = validated_data.pop("order_products")
        order = Orders.objects.create(**validated_data)
        for product in products_data:
            OrderProducts.objects.create(order=order, **product)
        return order
