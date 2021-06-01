from users.models import AutoUser
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
    autouser = serializers.CharField()

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

    def validate_autouser(self, value):
        return value

    def create(self, validated_data):
        products_data = validated_data.pop("order_products")
        autouser = validated_data.pop("autouser")
        qs = AutoUser.objects.get(userId=autouser)
        validated_data["autouser"] = qs
        print(validated_data)

        order = Orders.objects.create(**validated_data)
        for product in products_data:
            OrderProducts.objects.create(order=order, **product)
        return order
