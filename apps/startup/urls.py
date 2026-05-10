from django.urls import path

from apps.startup.views import StartupProfileView

urlpatterns = [
    path("profile/", StartupProfileView.as_view(), name="startup-profile"),
]
