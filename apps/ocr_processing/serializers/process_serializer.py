from rest_framework import serializers

from apps.ocr_processing.models import OCRProcessingRecord
from apps.ocr_processing.services.image_service import ImageService
from apps.ocr_processing.validators import validate_latitude, validate_longitude


class OCRProcessingCreateSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

    def validate_image(self, value):
        return ImageService.validate_image(value)

    def validate_lat(self, value):
        return validate_latitude(value)

    def validate_lon(self, value):
        return validate_longitude(value)


class OCRProcessingResponseSerializer(serializers.ModelSerializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = OCRProcessingRecord
        fields = [
            "id",
            "latitude",
            "longitude",
            "address",
            "extracted_text",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return None
        if request is None:
            return obj.image.url
        return request.build_absolute_uri(obj.image.url)

    def get_latitude(self, obj):
        return float(obj.latitude)

    def get_longitude(self, obj):
        return float(obj.longitude)
