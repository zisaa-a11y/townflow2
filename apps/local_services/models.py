from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)


class ServiceProvider(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_providers")
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="providers")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, db_index=True)


class ServiceBooking(BaseModel):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_bookings")
    scheduled_for = models.DateTimeField(db_index=True)
    notes = models.TextField(blank=True)
