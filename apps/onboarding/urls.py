from django.urls import path

from apps.onboarding.views import OnboardingProgressView

urlpatterns = [
    path("progress/", OnboardingProgressView.as_view(), name="onboarding-progress"),
]
