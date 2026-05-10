from rest_framework import serializers

from apps.blood_donation.models import BloodGroup, BloodRequest, DonorProfile


class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = ["id", "name"]


class DonorProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = DonorProfile
        fields = [
            "id",
            "user",
            "user_name",
            "blood_group",
            "last_donated_at",
            "is_available",
            "latitude",
            "longitude",
            "created_at",
        ]
        read_only_fields = ["id", "user", "user_name", "created_at"]


class BloodRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source="requester.full_name", read_only=True)

    class Meta:
        model = BloodRequest
        fields = [
            "id",
            "requester",
            "requester_name",
            "blood_group",
            "units_needed",
            "urgency",
            "status",
            "hospital_name",
            "required_by",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "requester", "requester_name", "created_at"]
