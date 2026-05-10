from rest_framework import serializers

from apps.local_services.models import ServiceBooking, ServiceCategory, ServiceProvider


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name"]


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = [
            "id",
            "owner",
            "category",
            "name",
            "description",
            "phone",
            "address",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "created_at"]


class ServiceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBooking
        fields = ["id", "provider", "user", "scheduled_for", "notes", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
