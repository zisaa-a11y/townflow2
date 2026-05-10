from django.conf import settings
from django.db import models

from common.constants.enums import IssueType, ReportStatus
from common.db.models import BaseModel
from common.validators.files import validate_image_upload


class IssueReport(BaseModel):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issue_reports")
    issue_type = models.CharField(max_length=20, choices=IssueType.CHOICES, db_index=True)
    status = models.CharField(max_length=20, choices=ReportStatus.CHOICES, default=ReportStatus.PENDING, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    photo = models.ImageField(upload_to="reports/", null=True, blank=True, validators=[validate_image_upload])

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["issue_type", "status", "created_at"])]


class IssueStatusLog(BaseModel):
    issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name="status_logs")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issue_status_updates")
    from_status = models.CharField(max_length=20, choices=ReportStatus.CHOICES)
    to_status = models.CharField(max_length=20, choices=ReportStatus.CHOICES)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
