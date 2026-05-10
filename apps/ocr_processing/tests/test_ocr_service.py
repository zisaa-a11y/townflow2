from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from apps.ocr_processing.services import OCRService, OCRServiceError


def build_test_image(name="ocr.png", image_format="PNG"):
    image = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    buffer.seek(0)
    return SimpleUploadedFile(name=name, content=buffer.read(), content_type="image/png")


class OCRServiceTests(TestCase):
    def setUp(self):
        self.service = OCRService()

    @patch("apps.ocr_processing.services.ocr_service.pytesseract.image_to_string")
    def test_extract_text_success(self, mock_image_to_string):
        mock_image_to_string.return_value = "  hello\n\n world  "
        result = self.service.extract_text(build_test_image())
        self.assertEqual(result, "hello\nworld")

    @patch("apps.ocr_processing.services.ocr_service.pytesseract.image_to_string")
    def test_extract_text_timeout(self, mock_image_to_string):
        mock_image_to_string.side_effect = RuntimeError("timeout")
        with self.assertRaises(OCRServiceError):
            self.service.extract_text(build_test_image())
