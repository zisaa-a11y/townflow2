from django.urls import path

from apps.home.views import HomeConfigView

urlpatterns = [
    path("config/", HomeConfigView.as_view(), name="home-config"),
]
