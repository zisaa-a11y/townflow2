from django.db import transaction

from apps.ocr_processing.constants import OCRProcessingStatus
from apps.ocr_processing.models import OCRProcessingRecord
from apps.ocr_processing.services.geocoding_service import GeocodingService, GeocodingServiceError
from apps.ocr_processing.services.image_service import ImageService
from apps.ocr_processing.services.ocr_service import OCRService, OCRServiceError


class ProcessingServiceError(Exception):
    pass


class ProcessingService:
    def __init__(self):
        self.image_service = ImageService()
        self.ocr_service = OCRService()
        self.geocoding_service = GeocodingService()

    @transaction.atomic
    def process_submission(self, *, image, latitude, longitude):
        self.image_service.validate_image(image)

        record = OCRProcessingRecord.objects.create(
            image=image,
            latitude=latitude,
            longitude=longitude,
            processing_status=OCRProcessingStatus.PROCESSING,
            metadata={},
        )

        try:
            extracted_text = self.ocr_service.extract_text(record.image)
            geocoded = self.geocoding_service.reverse_geocode(latitude, longitude)

            record.extracted_text = extracted_text
            record.address = geocoded.get("display_name") or geocoded.get("address_line", "")
            record.metadata = {
                "geocoding": {
                    "address_line": geocoded.get("address_line", ""),
                    "components": geocoded.get("components", {}),
                }
            }
            record.processing_status = OCRProcessingStatus.COMPLETED
            record.save(update_fields=["extracted_text", "address", "metadata", "processing_status", "updated_at"])
            return record
        except (OCRServiceError, GeocodingServiceError) as exc:
            record.processing_status = OCRProcessingStatus.FAILED
            record.metadata = {"error": str(exc)}
            record.save(update_fields=["processing_status", "metadata", "updated_at"])
            raise ProcessingServiceError(str(exc)) from exc
