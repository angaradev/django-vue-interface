from rest_framework import serializers
from .models import OrderProducts, Orders


class OrderProductsSerializer(serializers.ModelSerializer):
    # order = serializers.IntegerField(required=False)

    class Meta:
        model = OrderProducts
        fields = [
            "product_name",
            "product_price",
            "order",
            "product_id",
            "product_car",
            "product_brand",
            "product_image",
            "product_slug",
            "qty",
        ]
        extra_kwargs = {
            "order": {"required": False, "allow_null": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductsSerializer(many=True)

    class Meta:
        model = Orders
        fields = [
            "id",
            "date",
            "number",
            "status",
            "delivery",
            "payment",
            "total_front",
            "city",
            "address",
            "phone",
            "email",
            "user",
            "total",
            "autouser",
            "order_products",
        ]

    def create(self, validated_data):
        products_data = validated_data.pop("order_products")

        order = Orders.objects.create(**validated_data)
        for product in products_data:
            OrderProducts.objects.create(order=order, **product)
        return order
