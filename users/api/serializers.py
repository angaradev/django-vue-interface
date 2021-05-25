from rest_framework import serializers
from users.models import CustomUser, UserAdresses


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdresses
        exclude = ("autouser",)
        extra_kwargs = {
            "zip_code": {"required": False, "allow_null": True},
            "city": {"required": False, "allow_null": True},
            "default": {"required": False, "allow_null": True},
        }


class UserDisplaySerializer(serializers.ModelSerializer):
    address_user = UserAddressSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        # fields = ("id", "email", "profile")
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "is_superuser",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = CustomUser(username=username, email=email, password=password)
        user.save()
        return user

    def update(self, instance, validated_data):
        print(instance.profile.phone)

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        try:
            instance.profile.phone = validated_data["profile"]["phone"]
        except:
            pass

        try:
            instance.profile.image = (
                validated_data["profile"]["image"] or instance.profile.image
            )
        except:
            pass
        instance.profile.save()
        instance.save()

        return instance
