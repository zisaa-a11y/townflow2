from django.db import models

from apps.ocr_processing.constants import OCRProcessingStatus
from apps.ocr_processing.utils import ocr_image_upload_path
from apps.ocr_processing.validators import validate_ocr_image_upload
from common.db.models import BaseModel


class OCRProcessingRecord(BaseModel):
    image = models.ImageField(upload_to=ocr_image_upload_path, validators=[validate_ocr_image_upload])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    address = models.TextField(blank=True)
    extracted_text = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    processing_status = models.CharField(
        max_length=20,
        choices=OCRProcessingStatus.CHOICES,
        default=OCRProcessingStatus.PENDING,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["processing_status", "created_at"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"OCRProcessingRecord<{self.id}>"
