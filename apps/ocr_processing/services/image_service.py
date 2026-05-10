from pathlib import Path

from django.conf import settings
from PIL import Image, UnidentifiedImageError
from rest_framework import serializers


class ImageService:
    @staticmethod
    def validate_image(file_obj):
        if not file_obj:
            raise serializers.ValidationError({"image": ["Image file is required."]})

        max_size_mb = settings.OCR_MAX_IMAGE_SIZE_MB
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_obj.size > max_size_bytes:
            raise serializers.ValidationError({"image": [f"Image size must not exceed {max_size_mb}MB."]})

        extension = Path(file_obj.name).suffix.lower().lstrip(".")
        if extension not in settings.OCR_ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                {
                    "image": [
                        "Unsupported image format. Allowed formats: "
                        + ", ".join(sorted(settings.OCR_ALLOWED_IMAGE_EXTENSIONS))
                        + "."
                    ]
                }
            )

        try:
            cursor = file_obj.tell() if hasattr(file_obj, "tell") else 0
            image = Image.open(file_obj)
            image.verify()
            if image.format and image.format.lower() not in settings.OCR_ALLOWED_IMAGE_EXTENSIONS:
                raise serializers.ValidationError({"image": ["Corrupted or unsupported image file."]})
        except UnidentifiedImageError as exc:
            raise serializers.ValidationError({"image": ["Invalid image file."]}) from exc
        finally:
            if hasattr(file_obj, "seek"):
                file_obj.seek(cursor)

        return file_obj
