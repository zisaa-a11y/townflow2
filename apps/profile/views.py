from apps.blood_donation.models import DonorProfile
from apps.community_feed.models import Post
from apps.ocr_processing.services.geocoding_service import GeocodingService, GeocodingServiceError
from apps.profile.models import DeviceToken, UserProfile
from apps.profile.serializers import DeviceTokenSerializer, MeSerializer, MeStatsSerializer, UserProfileSerializer
from apps.report_issues.models import IssueReport
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class MeDetailUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(
            {
                "id": str(request.user.id),
                "email": request.user.email,
                "full_name": request.user.full_name,
                "phone": request.user.phone,
                "role": request.user.role,
                "is_verified": request.user.is_verified,
                "location_label": profile.location_label,
                "latitude": profile.latitude,
                "longitude": profile.longitude,
                "push_notifications_enabled": profile.push_notifications_enabled,
                "location_services_enabled": profile.location_services_enabled,
            }
        )

    def patch(self, request):
        serializer = MeSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        validated = serializer.validated_data

        for field in ["email", "full_name", "phone"]:
            if field in validated:
                setattr(request.user, field, validated[field])
        request.user.save(update_fields=[f for f in ["email", "full_name", "phone"] if f in validated] + ["updated_at"])

        for field in ["location_label", "push_notifications_enabled", "location_services_enabled"]:
            if field in validated:
                setattr(profile, field, validated[field])
        profile.save(
            update_fields=[
                f
                for f in ["location_label", "push_notifications_enabled", "location_services_enabled"]
                if f in validated
            ]
            + ["updated_at"]
        )

        return self.get(request)


class MeStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "posts_count": Post.objects.filter(author=request.user).count(),
            "donations_count": DonorProfile.objects.filter(user=request.user).count(),
            "reports_count": IssueReport.objects.filter(reporter=request.user).count(),
        }
        serializer = MeStatsSerializer(data)
        return Response(serializer.data)


class MeDeviceListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeviceToken.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MeDeviceDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        deleted, _ = DeviceToken.objects.filter(id=pk, user=request.user).delete()
        if not deleted:
            return Response({"detail": "Device token not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeLocationUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        location_label = request.data.get("location_label", "")

        if latitude is None or longitude is None:
            return Response(
                {"detail": "latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.latitude = latitude
        profile.longitude = longitude
        if location_label is not None:
            profile.location_label = location_label
        profile.save(update_fields=["latitude", "longitude", "location_label", "updated_at"])
        return Response(UserProfileSerializer(profile).data)


class ReverseLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        latitude = request.query_params.get("lat")
        longitude = request.query_params.get("lon")
        if latitude is None or longitude is None:
            return Response(
                {"detail": "lat and lon query params are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = GeocodingService()
        try:
            data = service.reverse_geocode(latitude=latitude, longitude=longitude)
        except GeocodingServiceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class ProfileDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
