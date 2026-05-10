from django.urls import path

from apps.authentication.views import (
    CustomTokenRefreshView,
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
    RequestOtpView,
    VerifyOtpView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("otp/request/", RequestOtpView.as_view(), name="otp-request"),
    path("otp/verify/", VerifyOtpView.as_view(), name="otp-verify"),
    path("me/", MeView.as_view(), name="me"),
]
