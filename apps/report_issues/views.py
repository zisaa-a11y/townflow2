from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.report_issues.models import IssueReport, IssueStatusLog
from apps.report_issues.serializers import IssueReportSerializer
from common.constants.enums import ReportStatus, UserRole
from common.constants.messages import ApiMessage
from common.permissions.rbac import IsAdminOrModerator


class IssueReportViewSet(viewsets.ModelViewSet):
    serializer_class = IssueReportSerializer
    filterset_fields = ["issue_type", "status"]
    search_fields = ["title", "description", "address"]
    ordering_fields = ["created_at", "updated_at"]

    def get_permissions(self):
        if self.action in {"update_status"}:
            return [permissions.IsAuthenticated(), IsAdminOrModerator()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = IssueReport.objects.select_related("reporter").prefetch_related("status_logs")
        if self.request.user.role in {UserRole.ADMIN, UserRole.MODERATOR}:
            return queryset
        return queryset.filter(reporter=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        report = self.get_object()
        old_status = report.status
        new_status = request.data.get("status", old_status)
        note = request.data.get("note", "")

        if new_status not in dict(ReportStatus.CHOICES):
            return Response(
                {"success": False, "message": ApiMessage.VALIDATION_ERROR, "errors": {"status": ["Invalid status"]}},
                status=400,
            )

        report.status = new_status
        report.save(update_fields=["status", "updated_at"])
        IssueStatusLog.objects.create(
            issue=report,
            updated_by=request.user,
            from_status=old_status,
            to_status=new_status,
            note=note,
        )
        return Response(self.get_serializer(report).data)
