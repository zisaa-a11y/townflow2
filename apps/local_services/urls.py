from rest_framework.routers import DefaultRouter

from apps.local_services.views import ServiceBookingViewSet, ServiceCategoryViewSet, ServiceProviderViewSet

router = DefaultRouter()
router.register("categories", ServiceCategoryViewSet, basename="service-categories")
router.register("providers", ServiceProviderViewSet, basename="service-providers")
router.register("bookings", ServiceBookingViewSet, basename="service-bookings")

urlpatterns = router.urls
