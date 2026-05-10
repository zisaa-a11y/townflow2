from rest_framework import serializers

from apps.digital_library.models import LibraryResource, ResourceProgress


class LibraryResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryResource
        fields = [
            "id",
            "title",
            "description",
            "category",
            "file_url",
            "cover_image_url",
            "uploaded_by",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "uploaded_by", "created_at"]


class ResourceProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceProgress
        fields = ["id", "resource", "user", "progress_percent", "is_downloaded", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
