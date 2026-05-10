from django.core.exceptions import ValidationError

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_SIZE_MB = 5


def validate_image_upload(value):
    extension = value.name.split(".")[-1].lower() if "." in value.name else ""
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Unsupported image format.")

    max_bytes = MAX_IMAGE_SIZE_MB * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError("Image file is too large.")
