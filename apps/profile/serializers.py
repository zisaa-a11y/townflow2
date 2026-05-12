from rest_framework import serializers

from apps.profile.models import DeviceToken, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "location_label",
            "latitude",
            "longitude",
            "push_notifications_enabled",
            "location_services_enabled",
            "posts_count",
            "donations_count",
            "reports_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "posts_count", "donations_count", "reports_count", "created_at", "updated_at"]


class MeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False, max_length=150)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    location_label = serializers.CharField(required=False, allow_blank=True, max_length=150)
    push_notifications_enabled = serializers.BooleanField(required=False)
    location_services_enabled = serializers.BooleanField(required=False)


class MeStatsSerializer(serializers.Serializer):
    posts_count = serializers.IntegerField()
    donations_count = serializers.IntegerField()
    reports_count = serializers.IntegerField()


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ["id", "token", "platform", "device_name", "created_at"]
        read_only_fields = ["id", "created_at"]
