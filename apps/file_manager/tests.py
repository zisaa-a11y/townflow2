"""
Tests for File Manager App
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from apps.authentication.models import User
from apps.file_manager.models import UploadedFile


class UploadedFileModelTest(TestCase):
    """Test cases for UploadedFile model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_create_uploaded_file(self):
        """Test creating an uploaded file"""
        file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")
        uploaded_file = UploadedFile.objects.create(
            file=file,
            title="Test File",
            description="A test file",
            category="document",
            file_size=file.size,
            file_type="text/plain",
            uploaded_by=self.user,
        )
        self.assertEqual(uploaded_file.title, "Test File")
        self.assertEqual(uploaded_file.category, "document")
        self.assertEqual(uploaded_file.uploaded_by, self.user)


class UploadedFileAPITest(APITestCase):
    """Test cases for File Manager API"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.client.force_authenticate(user=self.user)

    def test_file_upload(self):
        """Test file upload endpoint"""
        file = SimpleUploadedFile("test.pdf", b"pdf content", content_type="application/pdf")
        data = {
            "file": file,
            "title": "Test PDF",
            "description": "A test PDF file",
            "category": "document",
            "is_public": False,
        }
        response = self.client.post("/api/v1/file-manager/files/", data, format="multipart")
        self.assertEqual(response.status_code, 201)

    def test_list_user_files(self):
        """Test listing user's files"""
        response = self.client.get("/api/v1/file-manager/files/my_files/")
        self.assertEqual(response.status_code, 200)
