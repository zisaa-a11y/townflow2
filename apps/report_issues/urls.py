from rest_framework.routers import DefaultRouter

from apps.report_issues.views import IssueReportViewSet

router = DefaultRouter()
router.register("", IssueReportViewSet, basename="report-issues")

urlpatterns = router.urls
