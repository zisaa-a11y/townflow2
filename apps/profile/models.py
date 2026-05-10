from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    location_label = models.CharField(max_length=150, blank=True)
    push_notifications_enabled = models.BooleanField(default=True)
    location_services_enabled = models.BooleanField(default=True)
    posts_count = models.PositiveIntegerField(default=0)
    donations_count = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["user", "location_label"])]
