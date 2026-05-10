from rest_framework import serializers

from apps.alerts.models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["id", "type", "title", "body", "is_read", "target_type", "target_id", "created_at"]
        read_only_fields = ["id", "created_at"]
