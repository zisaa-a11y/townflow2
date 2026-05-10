from rest_framework import permissions, viewsets

from apps.digital_library.models import LibraryResource, ResourceProgress
from apps.digital_library.serializers import LibraryResourceSerializer, ResourceProgressSerializer


class LibraryResourceViewSet(viewsets.ModelViewSet):
    serializer_class = LibraryResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "is_active"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return LibraryResource.objects.select_related("uploaded_by").prefetch_related("progress_records")

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class ResourceProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["resource", "is_downloaded"]

    def get_queryset(self):
        return ResourceProgress.objects.select_related("resource", "user")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
