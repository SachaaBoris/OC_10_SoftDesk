"""
Provides serializers for objects of "Users" application.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from .checker import check_user_email_exist


class SignUpSerializer(serializers.ModelSerializer):
    """Sign up serializer."""

    class Meta:
        model = User
        fields = ("email", "username", "password", "age")
        extra_kwargs = {
            "password": {"write_only": True},
            "age": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        return User.objects.create_user(password=password, **validated_data)

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        validate_password(password=password, user=user)

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    """User object serializer."""

    class Meta:
        model = User
        fields = ("email", "username", "password", "age")

    def validate(self, attrs):
        user = User(**attrs)
        password = self.context["request"].data["password"]
        validate_password(password=password, user=user)

        return super().validate(attrs)
