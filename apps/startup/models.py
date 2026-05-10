from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class StartupProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="startup_profile")
    contact_method = models.CharField(max_length=20, blank=True)
    location_label = models.CharField(max_length=150, blank=True)
    otp_verified = models.BooleanField(default=False, db_index=True)
