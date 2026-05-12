from django.urls import path

from apps.authentication.views import (
    CustomTokenRefreshView,
    ForgotPasswordView,
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
    ResendOtpView,
    RequestOtpView,
    VerifyOtpView,
)

urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="refresh"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("resend-otp/", ResendOtpView.as_view(), name="resend-otp"),
    path("otp/request/", RequestOtpView.as_view(), name="otp-request"),
    path("otp/verify/", VerifyOtpView.as_view(), name="otp-verify"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("me/", MeView.as_view(), name="me"),
]
