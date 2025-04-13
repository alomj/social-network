from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import user
from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(token)

        token['username'] = user.username
        token['password'] = user.password

        return token


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError('Passwords must match')
        return data

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Email cannot be empty')
        return value

