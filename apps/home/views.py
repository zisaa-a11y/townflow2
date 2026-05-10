from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.home.models import HomeBanner, QuickAction
from apps.home.serializers import HomeBannerSerializer, QuickActionSerializer


class HomeConfigView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        banners = HomeBanner.objects.filter(is_active=True).order_by("-created_at")
        actions = QuickAction.objects.filter(is_active=True)
        return Response(
            {
                "banners": HomeBannerSerializer(banners, many=True).data,
                "quick_actions": QuickActionSerializer(actions, many=True).data,
            }
        )
