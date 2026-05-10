from rest_framework import serializers

from apps.onboarding.models import OnboardingProgress


class OnboardingProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingProgress
        fields = ["id", "is_completed", "completed_step", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
