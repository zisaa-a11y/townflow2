from rest_framework.routers import DefaultRouter

from apps.splash.views import AppReleaseViewSet

router = DefaultRouter()
router.register("releases", AppReleaseViewSet, basename="app-releases")

urlpatterns = router.urls
