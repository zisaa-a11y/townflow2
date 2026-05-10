from rest_framework import serializers

from apps.profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "location_label",
            "push_notifications_enabled",
            "location_services_enabled",
            "posts_count",
            "donations_count",
            "reports_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "posts_count", "donations_count", "reports_count", "created_at", "updated_at"]
