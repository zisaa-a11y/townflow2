from rest_framework import serializers

from apps.startup.models import StartupProfile


class StartupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupProfile
        fields = ["id", "contact_method", "location_label", "otp_verified", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
