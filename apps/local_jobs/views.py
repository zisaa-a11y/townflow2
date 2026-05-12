from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.local_jobs.models import Job, JobApplication
from apps.local_jobs.serializers import JobApplicationSerializer, JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["job_type", "is_active"]
    search_fields = ["title", "description", "company_name", "location"]

    def get_queryset(self):
        return Job.objects.select_related("posted_by").prefetch_related("applications")

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="apply")
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = JobApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(job=job, applicant=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["job"]

    def get_queryset(self):
        return JobApplication.objects.select_related("job", "applicant")

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)
