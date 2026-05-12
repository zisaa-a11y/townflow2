from django.urls import path

from apps.profile.views import (
    MeDetailUpdateView,
    MeDeviceDeleteView,
    MeDeviceListCreateView,
    MeLocationUpdateView,
    MeStatsView,
    ProfileDetailUpdateView,
    ReverseLocationView,
)

urlpatterns = [
    path("", MeDetailUpdateView.as_view(), name="me"),
    path("stats/", MeStatsView.as_view(), name="me-stats"),
    path("devices/", MeDeviceListCreateView.as_view(), name="me-devices"),
    path("devices/<uuid:pk>/", MeDeviceDeleteView.as_view(), name="me-device-delete"),
    path("location/", MeLocationUpdateView.as_view(), name="me-location"),
    path("reverse-location/", ReverseLocationView.as_view(), name="location-reverse"),
    path("me/", ProfileDetailUpdateView.as_view(), name="profile-me"),
]
