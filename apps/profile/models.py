from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class UserProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    location_label = models.CharField(max_length=150, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    push_notifications_enabled = models.BooleanField(default=True)
    location_services_enabled = models.BooleanField(default=True)
    posts_count = models.PositiveIntegerField(default=0)
    donations_count = models.PositiveIntegerField(default=0)
    reports_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["user", "location_label"])]


class DeviceToken(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens")
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=20, blank=True)
    device_name = models.CharField(max_length=100, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
