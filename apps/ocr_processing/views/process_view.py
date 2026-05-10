from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.ocr_processing.permissions import IsOCRProcessorAllowed
from apps.ocr_processing.serializers import OCRProcessingCreateSerializer, OCRProcessingResponseSerializer
from apps.ocr_processing.services import ProcessingService, ProcessingServiceError


class OCRProcessAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOCRProcessorAllowed]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ocr_processing"

    @extend_schema(
        tags=["OCR Processing"],
        request=OCRProcessingCreateSerializer,
        responses={
            201: OpenApiResponse(response=OCRProcessingResponseSerializer, description="Image processed successfully"),
            400: OpenApiResponse(description="Processing failed"),
        },
        examples=[
            OpenApiExample(
                "Request example",
                value={
                    "image": "<binary>",
                    "lat": "23.000000",
                    "lon": "90.000000",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Successful response",
                value={
                    "success": True,
                    "message": "Image processed successfully",
                    "data": {
                        "id": "33d4c87f-7dc7-41fc-a16f-0f6f6962537d",
                        "latitude": 23.0,
                        "longitude": 90.0,
                        "address": "Dhaka, Bangladesh",
                        "extracted_text": "Sample OCR text",
                        "image_url": "http://localhost:8000/media/ocr-processing/2026/05/10/sample.jpg",
                        "created_at": "2026-05-10T10:00:00Z",
                    },
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Failure response",
                value={
                    "success": False,
                    "message": "Processing failed",
                    "errors": {"detail": ["Reverse geocoding provider is temporarily unavailable."]},
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    def post(self, request):
        serializer = OCRProcessingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProcessingService()
        validated = serializer.validated_data

        try:
            record = service.process_submission(
                image=validated["image"],
                latitude=validated["lat"],
                longitude=validated["lon"],
            )
        except ProcessingServiceError as exc:
            return Response(
                {
                    "success": False,
                    "message": "Processing failed",
                    "errors": {"detail": [str(exc)]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = OCRProcessingResponseSerializer(record, context={"request": request}).data
        return Response(
            {
                "success": True,
                "message": "Image processed successfully",
                "data": response_data,
            },
            status=status.HTTP_201_CREATED,
        )
