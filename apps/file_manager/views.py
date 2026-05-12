from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.file_manager.models import FileAccessLog, UploadedFile
from apps.file_manager.permissions import IsFileOwner, IsFileOwnerOrReadOnly
from apps.file_manager.serializers import FileAccessLogSerializer, FileUploadSerializer, UploadedFileSerializer


class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.select_related("uploaded_by").prefetch_related("access_logs")
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated, IsFileOwnerOrReadOnly]
    filterset_fields = ["category", "is_public", "uploaded_by"]
    search_fields = ["title", "description", "uploaded_by__username"]
    ordering_fields = ["created_at", "download_count", "file_size"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        # Show user's own files and public files
        if user.is_authenticated:
            from django.db.models import Q

            return UploadedFile.objects.filter(Q(uploaded_by=user) | Q(is_public=True)).select_related("uploaded_by")
        return UploadedFile.objects.filter(is_public=True)

    def get_serializer_class(self):
        if self.action == "create":
            return FileUploadSerializer
        return UploadedFileSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def download(self, request, pk=None):
        """Download a file and log the access"""
        file_obj = self.get_object()

        # Check permissions
        if not file_obj.is_public and file_obj.uploaded_by != request.user:
            return Response({"error": "You don't have permission to download this file."}, status=status.HTTP_403_FORBIDDEN)

        # Log the download
        FileAccessLog.objects.create(
            file=file_obj, accessed_by=request.user, action="download", ip_address=self._get_client_ip(request)
        )

        # Increment download count
        file_obj.increment_download_count()

        # Return file download response
        response = Response({"message": "Download counted", "file_url": file_obj.file.url})
        return response

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def access_logs(self, request, pk=None):
        """Get access logs for a file"""
        file_obj = self.get_object()

        # Only owner can view access logs
        if file_obj.uploaded_by != request.user:
            return Response({"error": "Only file owner can view access logs."}, status=status.HTTP_403_FORBIDDEN)

        logs = file_obj.access_logs.all()
        serializer = FileAccessLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_files(self, request):
        """Get all files uploaded by the current user"""
        queryset = UploadedFile.objects.filter(uploaded_by=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def public_files(self, request):
        """Get all public files"""
        queryset = UploadedFile.objects.filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def _get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
