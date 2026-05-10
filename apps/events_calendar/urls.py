from rest_framework.routers import DefaultRouter

from apps.events_calendar.views import EventViewSet

router = DefaultRouter()
router.register("events", EventViewSet, basename="events")

urlpatterns = router.urls
