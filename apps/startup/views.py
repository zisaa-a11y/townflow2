from rest_framework import generics

from apps.startup.models import StartupProfile
from apps.startup.serializers import StartupProfileSerializer


class StartupProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StartupProfileSerializer

    def get_object(self):
        profile, _ = StartupProfile.objects.get_or_create(user=self.request.user)
        return profile
