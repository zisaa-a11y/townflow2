from django.urls import include, path

from apps.blood_donation.views import BloodRequestViewSet, DonorProfileViewSet
from apps.community_feed.views import PostViewSet
from apps.events_calendar.views import EventViewSet
from apps.local_jobs.views import JobViewSet
from apps.local_services.views import ServiceBookingViewSet, ServiceProviderViewSet
from apps.profile.views import (
    MeDetailUpdateView,
    MeDeviceDeleteView,
    MeDeviceListCreateView,
    MeLocationUpdateView,
    MeStatsView,
    ReverseLocationView,
)
from apps.report_issues.views import IssueReportViewSet

feed_list = PostViewSet.as_view({"get": "list", "post": "create"})
feed_detail = PostViewSet.as_view({"get": "retrieve", "delete": "destroy"})
feed_like = PostViewSet.as_view({"post": "like", "delete": "like"})
feed_comments = PostViewSet.as_view({"get": "comments", "post": "comments"})

events_list = EventViewSet.as_view({"get": "list"})
events_detail = EventViewSet.as_view({"get": "retrieve"})
events_rsvp = EventViewSet.as_view({"post": "rsvp", "delete": "un_rsvp"})
me_events = EventViewSet.as_view({"get": "my_events"})

reports_list = IssueReportViewSet.as_view({"get": "list", "post": "create"})
report_detail = IssueReportViewSet.as_view({"get": "retrieve"})
me_reports = IssueReportViewSet.as_view({"get": "my_reports"})

donors_list = DonorProfileViewSet.as_view({"get": "list"})
donor_detail = DonorProfileViewSet.as_view({"get": "retrieve"})
blood_requests_list = BloodRequestViewSet.as_view({"get": "list", "post": "create"})
blood_request_detail = BloodRequestViewSet.as_view({"patch": "partial_update"})

jobs_list = JobViewSet.as_view({"get": "list"})
jobs_apply = JobViewSet.as_view({"post": "apply"})

service_providers_list = ServiceProviderViewSet.as_view({"get": "list"})
bookings_create = ServiceBookingViewSet.as_view({"post": "create"})

urlpatterns = [
    # Requested contract aliases
    path("me/", MeDetailUpdateView.as_view(), name="me"),
    path("me/stats/", MeStatsView.as_view(), name="me-stats"),
    path("me/devices/", MeDeviceListCreateView.as_view(), name="me-devices"),
    path("me/devices/<uuid:pk>/", MeDeviceDeleteView.as_view(), name="me-device-delete"),
    path("me/location/", MeLocationUpdateView.as_view(), name="me-location"),
    path("me/events/", me_events, name="me-events"),
    path("me/reports/", me_reports, name="me-reports"),
    path("location/reverse/", ReverseLocationView.as_view(), name="location-reverse"),

    path("feed/", feed_list, name="feed-list"),
    path("feed/<uuid:pk>/", feed_detail, name="feed-detail"),
    path("feed/<uuid:pk>/like/", feed_like, name="feed-like"),
    path("feed/<uuid:pk>/comments/", feed_comments, name="feed-comments"),

    path("events/", events_list, name="events-list"),
    path("events/<uuid:pk>/", events_detail, name="events-detail"),
    path("events/<uuid:pk>/rsvp/", events_rsvp, name="events-rsvp"),

    path("reports/", reports_list, name="reports-list"),
    path("reports/<uuid:pk>/", report_detail, name="reports-detail"),

    path("donors/", donors_list, name="donors-list"),
    path("donors/<uuid:pk>/", donor_detail, name="donors-detail"),
    path("blood-requests/", blood_requests_list, name="blood-requests-list"),
    path("blood-requests/<uuid:pk>/", blood_request_detail, name="blood-requests-detail"),

    path("jobs/", jobs_list, name="jobs-list"),
    path("jobs/<uuid:pk>/apply/", jobs_apply, name="jobs-apply"),
    path("services/providers/", service_providers_list, name="service-providers-list"),
    path("bookings/", bookings_create, name="bookings-create"),

    path("auth/", include("apps.authentication.urls")),
    path("alerts/", include("apps.alerts.urls")),
    path("blood-donation/", include("apps.blood_donation.urls")),
    path("community-feed/", include("apps.community_feed.urls")),
    path("digital-library/", include("apps.digital_library.urls")),
    path("events-calendar/", include("apps.events_calendar.urls")),
    path("file-manager/", include("apps.file_manager.urls")),
    path("home/", include("apps.home.urls")),
    path("local-jobs/", include("apps.local_jobs.urls")),
    path("local-services/", include("apps.local_services.urls")),
    path("onboarding/", include("apps.onboarding.urls")),
    path("ocr/", include("apps.ocr_processing.urls")),
    path("profile/", include("apps.profile.urls")),
    path("report-issues/", include("apps.report_issues.urls")),
    path("shell/", include("apps.shell.urls")),
    path("splash/", include("apps.splash.urls")),
    path("startup/", include("apps.startup.urls")),
    path("volunteer-hub/", include("apps.volunteer_hub.urls")),
]
