from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from .models import User


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_admin
        token['is_superuser'] = user.is_superuser
        # ...

        return token
    

class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self , value):
        if User.objects.filter(email = value).exists():
            raise ValidationError("ایمیل از قبل وجود دارد")
        return value

class UserRegisterVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField()

class UserRegisterCompleteSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] and attrs["password2"] and attrs["password"] != attrs["password2"]:
            raise ValidationError("رمزها با هم مطابقت ندارد")
        return super().validate(attrs)
