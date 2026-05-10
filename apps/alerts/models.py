from django.conf import settings
from django.db import models

from common.constants.enums import AlertType
from common.db.models import BaseModel


class Alert(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alerts")
    type = models.CharField(max_length=30, choices=AlertType.CHOICES, db_index=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    target_type = models.CharField(max_length=50, blank=True)
    target_id = models.UUIDField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read", "created_at"])]
