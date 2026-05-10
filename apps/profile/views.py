from rest_framework import generics

from apps.profile.models import UserProfile
from apps.profile.serializers import UserProfileSerializer


class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
