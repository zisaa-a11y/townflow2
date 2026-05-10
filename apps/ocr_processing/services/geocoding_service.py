import logging

import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class GeocodingServiceError(Exception):
    pass


class GeocodingService:
    def __init__(self):
        self.base_url = settings.NOMINATIM_BASE_URL
        self.timeout = settings.GEOCODING_TIMEOUT_SECONDS
        self.session = requests.Session()
        retries = Retry(
            total=settings.GEOCODING_RETRY_TOTAL,
            connect=settings.GEOCODING_RETRY_TOTAL,
            read=settings.GEOCODING_RETRY_TOTAL,
            backoff_factor=settings.GEOCODING_RETRY_BACKOFF,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _build_headers(self):
        return {
            "User-Agent": settings.NOMINATIM_USER_AGENT,
            "Referer": settings.NOMINATIM_REFERER,
            "Accept": "application/json",
            "Accept-Language": settings.GEOCODING_ACCEPT_LANGUAGE,
        }

    def _compose_address_line(self, address):
        locality = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet")
        parts = [
            address.get("road"),
            address.get("suburb") or address.get("neighbourhood"),
            locality,
            address.get("state"),
            address.get("postcode"),
            address.get("country"),
        ]
        return ", ".join([part for part in parts if part])

    def reverse_geocode(self, latitude, longitude):
        params = {
            "format": "jsonv2",
            "lat": str(latitude),
            "lon": str(longitude),
            "addressdetails": 1,
        }

        try:
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self._build_headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            logger.warning("Reverse geocoding request failed", exc_info=exc)
            raise GeocodingServiceError("Reverse geocoding provider is temporarily unavailable.") from exc
        except ValueError as exc:
            logger.warning("Reverse geocoding invalid JSON response", exc_info=exc)
            raise GeocodingServiceError("Reverse geocoding returned an invalid response.") from exc

        address = payload.get("address", {})
        address_line = self._compose_address_line(address)

        return {
            "display_name": payload.get("display_name") or address_line,
            "address_line": address_line,
            "components": address,
            "raw": payload,
        }
