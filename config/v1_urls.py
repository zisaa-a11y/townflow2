from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("alerts/", include("apps.alerts.urls")),
    path("blood-donation/", include("apps.blood_donation.urls")),
    path("community-feed/", include("apps.community_feed.urls")),
    path("digital-library/", include("apps.digital_library.urls")),
    path("events-calendar/", include("apps.events_calendar.urls")),
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
