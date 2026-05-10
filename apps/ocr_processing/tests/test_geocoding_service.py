from unittest.mock import Mock

import requests
from django.test import TestCase

from apps.ocr_processing.services import GeocodingService, GeocodingServiceError


class GeocodingServiceTests(TestCase):
    def setUp(self):
        self.service = GeocodingService()

    def test_reverse_geocode_success(self):
        response = Mock()
        response.raise_for_status = Mock()
        response.json.return_value = {
            "display_name": "Dhaka, Bangladesh",
            "address": {
                "city": "Dhaka",
                "state": "Dhaka Division",
                "country": "Bangladesh",
            },
        }
        self.service.session.get = Mock(return_value=response)

        result = self.service.reverse_geocode("23.810331", "90.412521")

        self.assertEqual(result["display_name"], "Dhaka, Bangladesh")
        self.assertEqual(result["components"]["city"], "Dhaka")

    def test_reverse_geocode_request_failure(self):
        self.service.session.get = Mock(side_effect=requests.Timeout("timeout"))

        with self.assertRaises(GeocodingServiceError):
            self.service.reverse_geocode("23.810331", "90.412521")
