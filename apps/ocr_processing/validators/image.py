from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_ocr_image_upload(value):
    extension = Path(value.name).suffix.lower().lstrip(".")
    if extension not in settings.OCR_ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Unsupported image format.")

    max_bytes = settings.OCR_MAX_IMAGE_SIZE_MB * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError("Image file is too large.")
