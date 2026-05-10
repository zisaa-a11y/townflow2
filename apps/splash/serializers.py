from rest_framework import serializers

from apps.splash.models import AppRelease


class AppReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppRelease
        fields = [
            "id",
            "platform",
            "current_version",
            "minimum_supported_version",
            "force_update",
            "release_notes",
            "updated_at",
        ]
