from rest_framework import serializers

from apps.shell.models import ShellPreference


class ShellPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShellPreference
        fields = ["id", "selected_tab", "alerts_unread_count", "updated_at"]
        read_only_fields = ["id", "updated_at"]
