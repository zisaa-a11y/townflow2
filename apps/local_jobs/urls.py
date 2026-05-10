from rest_framework.routers import DefaultRouter

from apps.local_jobs.views import JobApplicationViewSet, JobViewSet

router = DefaultRouter()
router.register("jobs", JobViewSet, basename="jobs")
router.register("applications", JobApplicationViewSet, basename="job-applications")

urlpatterns = router.urls
