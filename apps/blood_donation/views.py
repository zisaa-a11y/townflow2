from rest_framework import permissions, viewsets

from apps.blood_donation.models import BloodGroup, BloodRequest, DonorProfile
from apps.blood_donation.serializers import BloodGroupSerializer, BloodRequestSerializer, DonorProfileSerializer


class BloodGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BloodGroup.objects.all().order_by("name")
    serializer_class = BloodGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class DonorProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["blood_group", "is_available"]

    def get_queryset(self):
        return DonorProfile.objects.select_related("user", "blood_group")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BloodRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["blood_group", "urgency", "status"]
    ordering_fields = ["required_by", "created_at"]

    def get_queryset(self):
        return BloodRequest.objects.select_related("requester", "blood_group").prefetch_related("matches")

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
