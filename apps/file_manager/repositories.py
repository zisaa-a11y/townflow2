"""
File Manager Repositories
"""

from apps.file_manager.models import FileAccessLog, UploadedFile


class UploadedFileRepository:
    """Repository for file operations"""

    @staticmethod
    def get_user_files(user):
        """Get all files uploaded by a user"""
        return UploadedFile.objects.filter(uploaded_by=user)

    @staticmethod
    def get_public_files():
        """Get all public files"""
        return UploadedFile.objects.filter(is_public=True)

    @staticmethod
    def get_file_by_id(file_id):
        """Get a file by ID"""
        return UploadedFile.objects.get(id=file_id)

    @staticmethod
    def get_files_by_category(category):
        """Get files by category"""
        return UploadedFile.objects.filter(category=category)

    @staticmethod
    def create_file(user, file, title, description, category, is_public=False):
        """Create a new file record"""
        return UploadedFile.objects.create(
            file=file,
            title=title,
            description=description,
            category=category,
            file_size=file.size,
            file_type=file.content_type or "application/octet-stream",
            uploaded_by=user,
            is_public=is_public,
        )

    @staticmethod
    def delete_file(file_obj):
        """Delete a file and remove from storage"""
        file_obj.file.delete()
        file_obj.delete()


class FileAccessLogRepository:
    """Repository for access log operations"""

    @staticmethod
    def get_file_logs(file_obj):
        """Get access logs for a file"""
        return FileAccessLog.objects.filter(file=file_obj)

    @staticmethod
    def get_user_logs(user):
        """Get all access logs for a user"""
        return FileAccessLog.objects.filter(accessed_by=user)

    @staticmethod
    def create_log(file_obj, user, action, ip_address=None):
        """Create an access log entry"""
        return FileAccessLog.objects.create(
            file=file_obj,
            accessed_by=user,
            action=action,
            ip_address=ip_address,
        )
