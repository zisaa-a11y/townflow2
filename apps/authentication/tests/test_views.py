"""Tests for authentication module."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

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
        full_name='Test User',
        phone='+8801234567890',
        role='citizen'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Fixture providing authenticated API client."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.mark.django_db
class TestAuthentication:
    """Test suite for authentication endpoints."""

    def test_user_registration(self, api_client):
        """Test user registration."""
        response = api_client.post('/api/v1/auth/register/', {
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'full_name': 'New User',
            'phone': '+8801234567890',
            'role': 'citizen'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['success'] is True
        assert response.data['data']['email'] == 'newuser@example.com'
        assert response.data['data']['is_verified'] is False

    def test_user_login(self, api_client, user):
        """Test user login."""
        response = api_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'access' in response.data['data']
        assert 'refresh' in response.data['data']
        assert response.data['data']['user']['email'] == 'test@example.com'

    def test_user_login_invalid_password(self, api_client, user):
        """Test login with invalid password."""
        response = api_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['success'] is False

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user profile."""
        response = authenticated_client.get('/api/v1/auth/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['full_name'] == user.full_name

    def test_request_otp(self, authenticated_client):
        """Test requesting OTP."""
        response = authenticated_client.post('/api/v1/auth/otp/request/', {
            'channel': 'email'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert 'session_id' in response.data['data']
        assert response.data['data']['channel'] == 'email'

    def test_logout(self, authenticated_client):
        """Test user logout."""
        # Get a refresh token first
        login_response = authenticated_client.post('/api/v1/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpass123'
        })

        refresh_token = login_response.data['data']['refresh']

        # Logout
        response = authenticated_client.post('/api/v1/auth/logout/', {
            'refresh': refresh_token
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True


@pytest.mark.django_db
class TestUserModel:
    """Test suite for User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            email='user@example.com',
            password='pass123',
            full_name='Test User'
        )

        assert user.email == 'user@example.com'
        assert user.is_active is True
        assert user.is_verified is False

    def test_user_string_representation(self, user):
        """Test user string representation."""
        assert str(user) == user.email

    def test_user_role_assignment(self):
        """Test user role assignment."""
        user = User.objects.create_user(
            email='moderator@example.com',
            password='pass123',
            role='moderator'
        )

        assert user.role == 'moderator'

    def test_password_hashing(self):
        """Test that passwords are hashed."""
        password = 'plaintext123'
        user = User.objects.create_user(
            email='user@example.com',
            password=password
        )

        assert user.password != password
        assert user.check_password(password) is True
