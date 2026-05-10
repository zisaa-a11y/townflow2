from rest_framework import generics

from apps.onboarding.models import OnboardingProgress
from apps.onboarding.serializers import OnboardingProgressSerializer


class OnboardingProgressView(generics.RetrieveUpdateAPIView):
    serializer_class = OnboardingProgressSerializer

    def get_object(self):
        progress, _ = OnboardingProgress.objects.get_or_create(user=self.request.user)
        return progress
