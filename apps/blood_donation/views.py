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
        queryset = DonorProfile.objects.select_related("user", "blood_group")
        lat = self.request.query_params.get("lat")
        lon = self.request.query_params.get("lon")
        radius_km = self.request.query_params.get("radius")
        if lat is None or lon is None or radius_km is None:
            return queryset

        try:
            lat = float(lat)
            lon = float(lon)
            radius = max(float(radius_km), 0.1)
        except (TypeError, ValueError):
            return queryset.none()

        lat_delta = radius / 111.0
        lon_delta = radius / (111.0 * max(0.1, abs(lat)))
        return queryset.filter(
            latitude__isnull=False,
            longitude__isnull=False,
            latitude__gte=lat - lat_delta,
            latitude__lte=lat + lat_delta,
            longitude__gte=lon - lon_delta,
            longitude__lte=lon + lon_delta,
        )

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
