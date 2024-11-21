"""
Provides serializers for objects of "Users" application.
"""
from rest_framework import serializers
from .models import User

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les détails d'un utilisateur"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'un utilisateur"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'password', 'password_confirm', 
                 'can_be_contacted', 'can_data_be_shared']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            age=validated_data['age'],
            password=validated_data['password'],
            can_be_contacted=validated_data.get('can_be_contacted', False),
            can_data_be_shared=validated_data.get('can_data_be_shared', False)
        )
        return user

class UserListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des utilisateurs (admin seulement)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'is_active']
