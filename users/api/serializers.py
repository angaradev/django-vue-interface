from rest_framework import serializers
from users.models import CustomUser, UserAdresses, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ("id", "user")
        extra_kwargs = {
            "image": {"required": False, "allow_null": True},
            "phone": {"required": False, "allow_null": True},
        }


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdresses
        exclude = ("autouser",)
        extra_kwargs = {
            "zip_code": {"required": False, "allow_null": True},
            "city": {"required": False, "allow_null": True},
        }


class UserDisplaySerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
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
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
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
