from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RequestOtpSerializer,
    RegisterSerializer,
    UserSerializer,
    VerifyOtpSerializer,
)
from apps.authentication.services import blacklist_refresh_token, issue_otp_session, verify_otp_session
from common.constants.messages import ApiMessage


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        user = payload["user"]
        return Response(
            {
                "success": True,
                "message": ApiMessage.SUCCESS,
                "data": {
                    "access": payload["access"],
                    "refresh": payload["refresh"],
                    "user": UserSerializer(user).data,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blacklist_refresh_token(serializer.validated_data["refresh"])
        return Response({"success": True, "message": ApiMessage.SUCCESS, "data": None}, status=status.HTTP_200_OK)


class RequestOtpView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RequestOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.validated_data["channel"]
        otp_session = issue_otp_session(request.user, channel)

        # Integrate SMS/email provider here. Do not expose OTP in production responses.
        data = {"session_id": str(otp_session.id), "channel": channel}
        if settings.DEBUG:
            data["debug_otp"] = getattr(otp_session, "_plain_code", None)

        return Response({"success": True, "message": ApiMessage.SUCCESS, "data": data}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_valid = verify_otp_session(
            request.user,
            serializer.validated_data["channel"],
            serializer.validated_data["code"],
        )
        if not is_valid:
            return Response(
                {"success": False, "message": ApiMessage.VALIDATION_ERROR, "errors": {"code": ["Invalid OTP"]}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"success": True, "message": ApiMessage.SUCCESS, "data": {"verified": True}},
            status=status.HTTP_200_OK,
        )


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]
