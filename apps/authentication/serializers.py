from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import OtpSession, User
from common.constants.enums import OtpChannel


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone", "role", "is_verified", "created_at", "updated_at"]


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RequestOtpSerializer(serializers.Serializer):
    channel = serializers.ChoiceField(choices=OtpChannel.CHOICES)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    channel = serializers.ChoiceField(choices=OtpChannel.CHOICES, default=OtpChannel.EMAIL)


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    channel = serializers.ChoiceField(choices=OtpChannel.CHOICES)
    code = serializers.CharField(min_length=4, max_length=10)


class OtpSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpSession
        fields = ["id", "channel", "expires_at", "is_used", "created_at"]
