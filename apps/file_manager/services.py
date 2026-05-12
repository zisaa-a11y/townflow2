"""
File Manager Services
"""

from apps.file_manager.models import FileAccessLog, UploadedFile


class FileService:
    """Service for handling file operations"""

    @staticmethod
    def get_user_files(user):
        """Get all files uploaded by a user"""
        return UploadedFile.objects.filter(uploaded_by=user)

    @staticmethod
    def get_public_files():
        """Get all public files"""
        return UploadedFile.objects.filter(is_public=True)

    @staticmethod
    def get_file_storage_usage(user):
        """Get total storage used by a user"""
        from django.db.models import Sum

        total_size = UploadedFile.objects.filter(uploaded_by=user).aggregate(total=Sum("file_size"))["total"]
        return total_size or 0

    @staticmethod
    def delete_file(file_obj):
        """Delete a file and log the action"""
        file_obj.file.delete()
        file_obj.delete()

    @staticmethod
    def log_access(file_obj, user, action, ip_address=None):
        """Log file access"""
        return FileAccessLog.objects.create(file=file_obj, accessed_by=user, action=action, ip_address=ip_address)
