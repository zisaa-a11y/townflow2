from pathlib import Path
from uuid import uuid4

from django.utils import timezone


def ocr_image_upload_path(instance, filename):
    suffix = Path(filename).suffix.lower() or ".jpg"
    date_path = timezone.now().strftime("%Y/%m/%d")
    return f"ocr-processing/{date_path}/{uuid4().hex}{suffix}"
