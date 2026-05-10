from rest_framework.routers import DefaultRouter

from apps.alerts.views import AlertViewSet

router = DefaultRouter()
router.register("", AlertViewSet, basename="alerts")

urlpatterns = router.urls
