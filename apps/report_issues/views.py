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
        lat = self.request.query_params.get("lat")
        lon = self.request.query_params.get("lon")
        radius_km = self.request.query_params.get("radius", "10")

        if lat is not None and lon is not None:
            try:
                lat = float(lat)
                lon = float(lon)
                radius = max(float(radius_km), 0.1)
            except (TypeError, ValueError):
                return queryset.none()

            lat_delta = radius / 111.0
            lon_delta = radius / (111.0 * max(0.1, abs(lat)))
            queryset = queryset.filter(
                latitude__isnull=False,
                longitude__isnull=False,
                latitude__gte=lat - lat_delta,
                latitude__lte=lat + lat_delta,
                longitude__gte=lon - lon_delta,
                longitude__lte=lon + lon_delta,
            )
            return queryset

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

    @action(detail=False, methods=["get"], url_path="my-reports")
    def my_reports(self, request):
        queryset = IssueReport.objects.select_related("reporter").prefetch_related("status_logs").filter(
            reporter=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
