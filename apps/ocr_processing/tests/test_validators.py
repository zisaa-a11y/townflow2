from django.test import SimpleTestCase
from rest_framework import serializers

from apps.ocr_processing.validators import validate_latitude, validate_longitude


class CoordinateValidatorTests(SimpleTestCase):
    def test_valid_latitude_and_longitude(self):
        self.assertEqual(str(validate_latitude("90")), "90")
        self.assertEqual(str(validate_longitude("-180")), "-180")

    def test_invalid_latitude(self):
        with self.assertRaises(serializers.ValidationError):
            validate_latitude("90.1")

    def test_invalid_longitude(self):
        with self.assertRaises(serializers.ValidationError):
            validate_longitude("-180.1")
