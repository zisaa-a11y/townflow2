from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from apps.ocr_processing.serializers import OCRProcessingCreateSerializer


def build_test_image(name="sample.png", image_format="PNG"):
    image = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    buffer.seek(0)
    return SimpleUploadedFile(name=name, content=buffer.read(), content_type="image/png")


class OCRProcessingCreateSerializerTests(TestCase):
    def test_valid_payload(self):
        serializer = OCRProcessingCreateSerializer(
            data={
                "image": build_test_image(),
                "lat": "23.810331",
                "lon": "90.412521",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_coordinates(self):
        serializer = OCRProcessingCreateSerializer(
            data={
                "image": build_test_image(),
                "lat": "120.000000",
                "lon": "190.000000",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("lat", serializer.errors)
        self.assertIn("lon", serializer.errors)

    def test_invalid_image_extension(self):
        bad_file = SimpleUploadedFile("bad.txt", b"invalid", content_type="text/plain")
        serializer = OCRProcessingCreateSerializer(
            data={
                "image": bad_file,
                "lat": "23.810331",
                "lon": "90.412521",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("image", serializer.errors)
