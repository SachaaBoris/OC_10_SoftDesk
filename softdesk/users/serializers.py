"""
Provides serializers for objects of "Users" application.
"""
from rest_framework import serializers
from .models import User

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer pour les détails d'un utilisateur"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'dob', 'can_be_contacted', 'can_data_be_shared']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'un utilisateur"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'dob', 'password', 'password_confirm', 
                 'can_be_contacted', 'can_data_be_shared']

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Un utilisateur avec cet email existe déjà."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Un utilisateur avec ce nom d'utilisateur existe déjà."})
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})  
        
        user = User(dob=attrs['dob'])  # instance temporaire pour obtenir l'age
        if user.calculate_age() < 15:
            raise serializers.ValidationError({"dob": "L'utilisateur doit avoir au moins 15 ans."})
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            dob=validated_data['dob'],
            password=validated_data['password'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared']
        )
        return user

class UserListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des utilisateurs"""
    class Meta:
        model = User
        fields = ['id', 'username']
