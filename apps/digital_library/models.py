from django.conf import settings
from django.db import models

from common.constants.enums import LibraryCategory
from common.db.models import BaseModel


class LibraryResource(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=LibraryCategory.CHOICES, db_index=True)
    file_url = models.URLField()
    cover_image_url = models.URLField(blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="library_resources")
    is_active = models.BooleanField(default=True, db_index=True)


class ResourceProgress(BaseModel):
    resource = models.ForeignKey(LibraryResource, on_delete=models.CASCADE, related_name="progress_records")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resource_progress")
    progress_percent = models.PositiveSmallIntegerField(default=0)
    is_downloaded = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["resource", "user"], name="unique_resource_progress")]
