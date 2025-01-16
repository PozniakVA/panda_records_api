from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return attrs


class ChangeEmailRequestSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)

    def validate_new_email(self, value):
        User = get_user_model()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Цей email уже використовується.")
        return value


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = ["password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
