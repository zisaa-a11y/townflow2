from rest_framework import permissions, viewsets

from apps.local_services.models import ServiceBooking, ServiceCategory, ServiceProvider
from apps.local_services.serializers import (
    ServiceBookingSerializer,
    ServiceCategorySerializer,
    ServiceProviderSerializer,
)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all().order_by("name")
    serializer_class = ServiceCategorySerializer


class ServiceProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "description", "address"]

    def get_queryset(self):
        return ServiceProvider.objects.select_related("owner", "category").prefetch_related("bookings")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ServiceBookingViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceBookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["provider"]

    def get_queryset(self):
        return ServiceBooking.objects.select_related("provider", "user")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
