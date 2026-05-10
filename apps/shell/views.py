from rest_framework import generics

from apps.shell.models import ShellPreference
from apps.shell.serializers import ShellPreferenceSerializer


class ShellPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = ShellPreferenceSerializer

    def get_object(self):
        pref, _ = ShellPreference.objects.get_or_create(user=self.request.user)
        return pref
