from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class ShellPreference(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shell_preference")
    selected_tab = models.CharField(max_length=50, blank=True)
    alerts_unread_count = models.PositiveIntegerField(default=0)
