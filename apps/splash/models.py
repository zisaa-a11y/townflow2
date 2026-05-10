from django.db import models

from common.db.models import BaseModel


class AppRelease(BaseModel):
    platform = models.CharField(max_length=20, db_index=True)
    current_version = models.CharField(max_length=40)
    minimum_supported_version = models.CharField(max_length=40)
    force_update = models.BooleanField(default=False)
    release_notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["platform", "current_version"])]
