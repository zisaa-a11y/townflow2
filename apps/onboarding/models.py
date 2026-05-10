from django.conf import settings
from django.db import models

from common.db.models import BaseModel


class OnboardingProgress(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="onboarding_progress")
    is_completed = models.BooleanField(default=False, db_index=True)
    completed_step = models.PositiveSmallIntegerField(default=0)
