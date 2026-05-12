"""Tests for OCR processing module."""

import io
import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.ocr_processing.models import OCRProcessingRecord
from apps.ocr_processing.constants import OCRProcessingStatus

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture providing an API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Fixture creating a test user."""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        full_name='Test User'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture providing authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


def create_test_image():
    """Helper to create a test image file."""
    image = Image.new('RGB', (100, 100), color='red')
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return SimpleUploadedFile(
        'test.jpg',
        image_io.getvalue(),
        content_type='image/jpeg'
    )


@pytest.mark.django_db
class TestOCRProcessing:
    """Test suite for OCR processing endpoints."""

    def test_process_image_success(self, authenticated_client):
        """Test successful image processing."""
        image = create_test_image()

        response = authenticated_client.post('/api/v1/ocr/process/', {
            'image': image,
            'lat': '23.8103',
            'lon': '90.4125'
        }, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert 'data' in response.data

    def test_process_image_invalid_coordinates_latitude(self, authenticated_client):
        """Test processing with invalid latitude."""
        image = create_test_image()

        response = authenticated_client.post('/api/v1/ocr/process/', {
            'image': image,
            'lat': '91.0000',  # Invalid: > 90
            'lon': '90.4125'
        }, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_process_image_invalid_coordinates_longitude(self, authenticated_client):
        """Test processing with invalid longitude."""
        image = create_test_image()

        response = authenticated_client.post('/api/v1/ocr/process/', {
            'image': image,
            'lat': '23.8103',
            'lon': '181.0000'  # Invalid: > 180
        }, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_process_image_without_auth(self, api_client):
        """Test OCR processing without authentication."""
        image = create_test_image()

        response = api_client.post('/api/v1/ocr/process/', {
            'image': image,
            'lat': '23.8103',
            'lon': '90.4125'
        }, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_process_image_missing_image(self, authenticated_client):
        """Test processing without image."""
        response = authenticated_client.post('/api/v1/ocr/process/', {
            'lat': '23.8103',
            'lon': '90.4125'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_ocr_results(self, authenticated_client, user):
        """Test listing OCR results."""
        # Create some OCR records
        OCRProcessingRecord.objects.create(
            image=create_test_image(),
            latitude=23.8103,
            longitude=90.4125,
            processing_status=OCRProcessingStatus.COMPLETED,
            address='Dhaka, Bangladesh'
        )

        response = authenticated_client.get('/api/v1/ocr/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True


@pytest.mark.django_db
class TestOCRModel:
    """Test suite for OCRProcessingRecord model."""

    def test_create_ocr_record(self):
        """Test creating an OCR record."""
        record = OCRProcessingRecord.objects.create(
            image=create_test_image(),
            latitude=23.8103,
            longitude=90.4125,
            processing_status=OCRProcessingStatus.PENDING
        )

        assert record.processing_status == OCRProcessingStatus.PENDING
        assert float(record.latitude) == 23.8103
        assert float(record.longitude) == 90.4125

    def test_ocr_record_status_transitions(self):
        """Test OCR record status transitions."""
        record = OCRProcessingRecord.objects.create(
            image=create_test_image(),
            latitude=23.8103,
            longitude=90.4125,
            processing_status=OCRProcessingStatus.PENDING
        )

        record.processing_status = OCRProcessingStatus.PROCESSING
        record.save()
        assert record.processing_status == OCRProcessingStatus.PROCESSING

        record.processing_status = OCRProcessingStatus.COMPLETED
        record.extracted_text = "Sample text from image"
        record.save()
        assert record.processing_status == OCRProcessingStatus.COMPLETED
