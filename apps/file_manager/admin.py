from django.contrib import admin

from apps.file_manager.models import FileAccessLog, UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "file_type", "file_size", "uploaded_by", "is_public", "created_at"]
    list_filter = ["category", "is_public", "created_at"]
    search_fields = ["title", "description", "uploaded_by__email"]
    readonly_fields = ["file_size", "file_type", "download_count", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("File Information", {"fields": ("file", "title", "description", "category")}),
        ("File Details", {"fields": ("file_size", "file_type", "download_count")}),
        ("Access Control", {"fields": ("uploaded_by", "is_public")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(FileAccessLog)
class FileAccessLogAdmin(admin.ModelAdmin):
    list_display = ["file", "accessed_by", "action", "created_at"]
    list_filter = ["action", "created_at"]
    search_fields = ["file__title", "accessed_by__email"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
