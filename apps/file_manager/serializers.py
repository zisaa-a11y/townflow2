from rest_framework import serializers

from apps.file_manager.models import FileAccessLog, UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source="uploaded_by.username", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "file",
            "file_url",
            "title",
            "description",
            "category",
            "file_size",
            "file_type",
            "uploaded_by",
            "uploaded_by_username",
            "is_public",
            "download_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "uploaded_by", "file_size", "file_type", "download_count", "created_at", "updated_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file:
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["file", "title", "description", "category", "is_public"]

    def validate(self, data):
        from apps.file_manager.validators import validate_file_upload

        file = data.get("file")
        category = data.get("category")

        if file and category:
            validate_file_upload(file, category)

        return data

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        validated_data["file_size"] = validated_data["file"].size
        validated_data["file_type"] = validated_data["file"].content_type or "application/octet-stream"
        return super().create(validated_data)


class FileAccessLogSerializer(serializers.ModelSerializer):
    file_title = serializers.CharField(source="file.title", read_only=True)
    accessed_by_username = serializers.CharField(source="accessed_by.username", read_only=True)

    class Meta:
        model = FileAccessLog
        fields = ["id", "file", "file_title", "accessed_by", "accessed_by_username", "action", "ip_address", "created_at"]
        read_only_fields = ["id", "created_at"]
