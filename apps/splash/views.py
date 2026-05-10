from rest_framework import permissions, viewsets

from apps.splash.models import AppRelease
from apps.splash.serializers import AppReleaseSerializer


class AppReleaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppReleaseSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["platform"]

    def get_queryset(self):
        return AppRelease.objects.order_by("-updated_at")
