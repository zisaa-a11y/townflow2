from django.core.exceptions import ValidationError

# File size limits (in bytes)
FILE_SIZE_LIMITS = {
    "document": 50 * 1024 * 1024,  # 50 MB
    "image": 20 * 1024 * 1024,  # 20 MB
    "video": 500 * 1024 * 1024,  # 500 MB
    "audio": 100 * 1024 * 1024,  # 100 MB
    "archive": 100 * 1024 * 1024,  # 100 MB
    "other": 10 * 1024 * 1024,  # 10 MB
}

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "document": {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/plain",
        "text/csv",
    },
    "image": {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"},
    "video": {"video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo", "video/webm"},
    "audio": {"audio/mpeg", "audio/wav", "audio/ogg", "audio/webm", "audio/aac"},
    "archive": {"application/zip", "application/x-rar-compressed", "application/x-7z-compressed", "application/gzip"},
}


def validate_file_upload(file, category):
    """Validate file upload based on category"""
    if file.size > FILE_SIZE_LIMITS.get(category, FILE_SIZE_LIMITS["other"]):
        raise ValidationError(f"File size exceeds the limit for {category} files.")

    if category in ALLOWED_MIME_TYPES:
        if hasattr(file, "content_type") and file.content_type not in ALLOWED_MIME_TYPES[category]:
            raise ValidationError(f"File type not allowed for {category} category.")
