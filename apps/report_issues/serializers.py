from rest_framework import serializers

from apps.report_issues.models import IssueReport, IssueStatusLog


class IssueStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueStatusLog
        fields = ["id", "from_status", "to_status", "note", "created_at"]
        read_only_fields = ["id", "created_at"]


class IssueReportSerializer(serializers.ModelSerializer):
    status_logs = IssueStatusLogSerializer(many=True, read_only=True)

    class Meta:
        model = IssueReport
        fields = [
            "id",
            "reporter",
            "issue_type",
            "status",
            "title",
            "description",
            "address",
            "latitude",
            "longitude",
            "photo",
            "status_logs",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reporter", "status_logs", "created_at", "updated_at"]
