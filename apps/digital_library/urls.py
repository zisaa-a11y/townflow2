from rest_framework.routers import DefaultRouter

from apps.digital_library.views import LibraryResourceViewSet, ResourceProgressViewSet

router = DefaultRouter()
router.register("resources", LibraryResourceViewSet, basename="library-resources")
router.register("progress", ResourceProgressViewSet, basename="resource-progress")

urlpatterns = router.urls
