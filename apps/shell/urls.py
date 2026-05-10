from django.urls import path

from apps.shell.views import ShellPreferenceView

urlpatterns = [
    path("preferences/", ShellPreferenceView.as_view(), name="shell-preferences"),
]
