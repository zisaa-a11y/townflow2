from django.conf import settings
from django.db import models

from common.constants.enums import FileCategory
from common.db.models import BaseModel
from common.storage.backends import PublicMediaStorage


def file_upload_path(instance, filename):
    """Generate file upload path based on file type and user"""
    return f"uploads/{instance.uploaded_by.id}/{instance.category}/{filename}"


class UploadedFile(BaseModel):
    CATEGORY_CHOICES = [
        ("document", "Document"),
        ("image", "Image"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("archive", "Archive"),
        ("other", "Other"),
    ]

    file = models.FileField(upload_to=file_upload_path, storage=PublicMediaStorage())
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    file_size = models.BigIntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=100, help_text="MIME type")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_files")
    is_public = models.BooleanField(default=False, db_index=True)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["uploaded_by", "-created_at"]),
            models.Index(fields=["category", "is_public"]),
        ]

    def __str__(self):
        return self.title

    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=["download_count"])


class FileAccessLog(BaseModel):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name="access_logs")
    accessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(
        max_length=20,
        choices=[("view", "Viewed"), ("download", "Downloaded"), ("delete", "Deleted")],
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["file", "-created_at"]),
            models.Index(fields=["accessed_by", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.file.title} - {self.action}"
