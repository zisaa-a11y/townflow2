from django.urls import path

from apps.profile.views import ProfileDetailUpdateView

urlpatterns = [
    path("me/", ProfileDetailUpdateView.as_view(), name="profile-me"),
]
