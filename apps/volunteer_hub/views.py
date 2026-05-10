from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.volunteer_hub.models import VolunteerEnrollment, VolunteerProject
from apps.volunteer_hub.serializers import VolunteerEnrollmentSerializer, VolunteerProjectSerializer


class VolunteerProjectViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status"]
    search_fields = ["title", "description", "location"]

    def get_queryset(self):
        return VolunteerProject.objects.select_related("organizer").prefetch_related("enrollments")

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=["get"], url_path="my-volunteering")
    def my_volunteering(self, request):
        queryset = self.get_queryset().filter(enrollments__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VolunteerEnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["project"]

    def get_queryset(self):
        return VolunteerEnrollment.objects.select_related("project", "user")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
