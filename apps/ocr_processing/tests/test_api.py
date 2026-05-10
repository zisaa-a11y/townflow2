from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from rest_framework.test import APIClient

from apps.ocr_processing.constants import OCRProcessingStatus
from apps.ocr_processing.models import OCRProcessingRecord


def build_test_image(name="api.png", image_format="PNG"):
    image = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    buffer.seek(0)
    return SimpleUploadedFile(name=name, content=buffer.read(), content_type="image/png")


class OCRProcessAPITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="ocr.user@example.com",
            password="StrongPass123",
            full_name="OCR User",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch("apps.ocr_processing.views.process_view.ProcessingService.process_submission")
    def test_process_endpoint_success(self, mock_process_submission):
        record = OCRProcessingRecord.objects.create(
            image=build_test_image("stored.png"),
            latitude="23.810331",
            longitude="90.412521",
            address="Dhaka, Bangladesh",
            extracted_text="Sample OCR text",
            processing_status=OCRProcessingStatus.COMPLETED,
            metadata={},
        )
        mock_process_submission.return_value = record

        response = self.client.post(
            "/api/v1/ocr/process/",
            data={"image": build_test_image(), "lat": "23.810331", "lon": "90.412521"},
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Image processed successfully")
        self.assertIn("data", response.data)

    @patch("apps.ocr_processing.views.process_view.ProcessingService.process_submission")
    def test_process_endpoint_failure(self, mock_process_submission):
        from apps.ocr_processing.services import ProcessingServiceError

        mock_process_submission.side_effect = ProcessingServiceError("processing unavailable")

        response = self.client.post(
            "/api/v1/ocr/process/",
            data={"image": build_test_image(), "lat": "23.810331", "lon": "90.412521"},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Processing failed")
