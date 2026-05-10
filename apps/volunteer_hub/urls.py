from rest_framework.routers import DefaultRouter

from apps.volunteer_hub.views import VolunteerEnrollmentViewSet, VolunteerProjectViewSet

router = DefaultRouter()
router.register("projects", VolunteerProjectViewSet, basename="volunteer-projects")
router.register("enrollments", VolunteerEnrollmentViewSet, basename="volunteer-enrollments")

urlpatterns = router.urls
