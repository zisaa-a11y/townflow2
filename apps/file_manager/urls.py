from rest_framework.routers import DefaultRouter

from apps.file_manager.views import UploadedFileViewSet

router = DefaultRouter()
router.register(r"files", UploadedFileViewSet, basename="file")

urlpatterns = router.urls
