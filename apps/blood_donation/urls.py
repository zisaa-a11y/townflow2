from rest_framework.routers import DefaultRouter

from apps.blood_donation.views import BloodGroupViewSet, BloodRequestViewSet, DonorProfileViewSet

router = DefaultRouter()
router.register("groups", BloodGroupViewSet, basename="blood-groups")
router.register("donors", DonorProfileViewSet, basename="donors")
router.register("requests", BloodRequestViewSet, basename="blood-requests")

urlpatterns = router.urls
