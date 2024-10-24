"""
Provides checker functions for "users" app.
"""
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import User


def check_user_email_exist(email):
    if not User.objects.filter(email=email):
        raise serializers.ValidationError(
            "Cet email d'utilisateur n'existe pas."
        )
