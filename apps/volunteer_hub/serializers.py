from rest_framework import serializers

from apps.volunteer_hub.models import VolunteerEnrollment, VolunteerProject


class VolunteerProjectSerializer(serializers.ModelSerializer):
    volunteers_count = serializers.IntegerField(source="enrollments.count", read_only=True)

    class Meta:
        model = VolunteerProject
        fields = [
            "id",
            "organizer",
            "title",
            "description",
            "location",
            "starts_at",
            "ends_at",
            "status",
            "volunteers_count",
            "created_at",
        ]
        read_only_fields = ["id", "organizer", "volunteers_count", "created_at"]


class VolunteerEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerEnrollment
        fields = ["id", "project", "user", "hours_contributed", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
