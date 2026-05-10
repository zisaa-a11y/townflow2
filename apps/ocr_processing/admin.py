from django.contrib import admin

from apps.ocr_processing.models import OCRProcessingRecord


@admin.register(OCRProcessingRecord)
class OCRProcessingRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "latitude", "longitude", "processing_status", "created_at")
    list_filter = ("processing_status", "created_at")
    search_fields = ("id", "address", "extracted_text")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
