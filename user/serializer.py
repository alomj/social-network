from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_username(value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value


    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value

    @staticmethod
    def validate_password(value):
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
        fields = ('username', 'email', 'first_name', 'last_name')


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

    @staticmethod
    def validate_email(value):
        if not value:
            raise serializers.ValidationError('Email cannot be empty')
        return value

