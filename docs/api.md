# TownFlow Backend API Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Backend Architecture](#backend-architecture)
3. [Modular App Structure](#modular-app-structure)
4. [Authentication & Authorization](#authentication--authorization)
5. [Core API Endpoints](#core-api-endpoints)
6. [Database Design](#database-design)
7. [Services Architecture](#services-architecture)
8. [Media Handling](#media-handling)
9. [Docker Setup](#docker-setup)
10. [Deployment & Operations](#deployment--operations)
11. [Development Guide](#development-guide)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)
14. [Scalability & Performance](#scalability--performance)

---

## Project Overview

**TownFlow** is an enterprise-grade community management platform that brings hyperlocal information, services, and engagement to neighborhoods. The backend is built on Django REST Framework with a production-ready architecture designed to handle scale, security, and maintainability.

### Key Features

- **Authentication System**: JWT-based authentication with email/OTP verification
- **User Profiles**: Comprehensive user profile management with location services
- **OCR Processing**: Image text extraction with automatic reverse geocoding
- **Community Feed**: Post creation, commenting, and like system
- **Events Management**: Event creation and RSVP tracking
- **Blood Donation Network**: Donor-request matching system
- **Issue Reporting**: Location-based issue tracking and resolution
- **Job Listings**: Local job opportunities with application tracking
- **Local Services**: Service provider discovery and booking
- **Device Management**: Multi-device push notification readiness
- **Admin Dashboard**: Moderator tools for content and user management

---

## Backend Architecture

### Technology Stack

```
Framework:       Django 5.1.9
REST Framework:  Django REST Framework 3.16
Database:        MySQL 8.0
Cache/Queue:     Redis 7.2
Authentication:  JWT (djangorestframework-simplejwt)
API Docs:        drf-spectacular (OpenAPI/Swagger)
Image Processing: Pillow, pytesseract
Geocoding:       Nominatim OpenStreetMap API
Deployment:      Docker, docker-compose, Gunicorn
```

### Architecture Principles

1. **Modular Design**: Each feature is a standalone Django app
2. **Service Layer**: Business logic separated from views
3. **Repository Pattern**: Database queries abstracted
4. **Centralized Exceptions**: Consistent error handling
5. **Role-Based Access Control**: Fine-grained permissions
6. **API Versioning**: Support for multiple API versions
7. **Horizontal Scaling**: Stateless design with Redis cache

### Directory Structure

```
Backend/
├── config/                    # Django settings and URL routing
│   ├── settings.py          # Main configuration
│   ├── urls.py              # Root URL patterns
│   ├── v1_urls.py           # API v1 routes
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── apps/                      # Feature modules
│   ├── authentication/        # JWT, login, signup, OTP
│   ├── profile/              # User profiles, preferences
│   ├── ocr_processing/       # Image text extraction
│   ├── community_feed/       # Posts, comments, likes
│   ├── events_calendar/      # Events, RSVP
│   ├── blood_donation/       # Donors, requests, matching
│   ├── report_issues/        # Issue reporting, status tracking
│   ├── local_jobs/           # Jobs, applications
│   ├── local_services/       # Services, bookings
│   ├── alerts/               # Alert management
│   └── [other apps]/         # Additional features
├── common/                    # Shared utilities
│   ├── db/                   # Base models, managers
│   ├── constants/            # Enums, messages
│   ├── exceptions/           # Exception handling
│   ├── permissions/          # Permission classes
│   ├── validators/           # Validation logic
│   ├── responses/            # Response formatters
│   ├── storage/              # File storage
│   ├── pagination.py         # Pagination classes
│   ├── filters.py            # Filter backends
│   └── [utilities]/          # Other utilities
├── static/                    # Static files (CSS, JS)
├── media/                     # User uploads
├── logs/                      # Application logs
├── requirements/              # Python dependencies
├── Dockerfile                 # Container image
├── docker-compose.yml         # Container orchestration
└── manage.py                  # Django management script
```

---

## Modular App Structure

Each Django app follows a consistent, scalable structure:

```
app_name/
├── models/                    # Database models
│   ├── __init__.py
│   └── [model_files].py
├── serializers/              # DRF serializers
│   ├── __init__.py
│   └── [serializer_files].py
├── views/                    # API views/viewsets
│   ├── __init__.py
│   └── [view_files].py
├── services/                 # Business logic
│   ├── __init__.py
│   └── [service_files].py
├── repositories/             # Database queries
│   ├── __init__.py
│   └── [repository_files].py
├── permissions/              # Custom permissions
│   ├── __init__.py
│   └── [permission_files].py
├── validators/              # Field validators
│   ├── __init__.py
│   └── [validator_files].py
├── constants/               # App constants
│   ├── __init__.py
│   └── [constant_files].py
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── [utility_files].py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_serializers.py
│   ├── test_views.py
│   ├── test_services.py
│   └── test_permissions.py
├── admin.py                 # Django admin
├── apps.py                  # App configuration
├── filters.py              # Query filters
├── models.py               # Legacy (imports from models/)
├── serializers.py          # Legacy (imports from serializers/)
├── urls.py                 # URL routing
└── views.py                # Legacy (imports from views/)
```

### Base Model Structure

All models inherit from `BaseModel` which provides:

```python
class BaseModel(UUIDPrimaryKeyModel, TimeStampedModel, SoftDeleteModel):
    """
    Base model with:
    - UUID primary key
    - created_at, updated_at timestamps
    - Soft delete support (is_deleted, deleted_at)
    """
    class Meta:
        abstract = True
```

#### UUIDPrimaryKeyModel
- Unique identifier: `id` (UUID4)
- Benefits: Security, distributed systems, no collision

#### TimeStampedModel
- `created_at`: DateTimeField, auto_now_add
- `updated_at`: DateTimeField, auto_now

#### SoftDeleteModel
- `is_deleted`: Boolean, default False
- `deleted_at`: DateTime, nullable
- Supports soft delete and recovery
- Custom manager filters deleted items by default

---

## Authentication & Authorization

### JWT Authentication Flow

#### 1. User Registration

**Endpoint:** `POST /api/v1/auth/register/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "phone": "+8801234567890",
  "role": "citizen"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Resource created successfully.",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+8801234567890",
    "role": "citizen",
    "is_verified": false,
    "created_at": "2026-05-12T10:00:00Z",
    "updated_at": "2026-05-12T10:00:00Z"
  }
}
```

#### 2. User Login

**Endpoint:** `POST /api/v1/auth/login/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "full_name": "John Doe",
      "phone": "+8801234567890",
      "role": "citizen",
      "is_verified": false,
      "created_at": "2026-05-12T10:00:00Z",
      "updated_at": "2026-05-12T10:00:00Z"
    }
  }
}
```

#### JWT Token Details

- **Access Token**: Valid for 30 minutes (configurable)
- **Refresh Token**: Valid for 7 days (configurable)
- **Auto-rotation**: Refresh token rotates on each refresh
- **Blacklist**: Old refresh tokens are blacklisted automatically

#### 3. Token Refresh

**Endpoint:** `POST /api/v1/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 4. OTP Verification Flow

**Step 1: Request OTP**

**Endpoint:** `POST /api/v1/auth/otp/request/`

**Request:**
```json
{
  "channel": "email"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "channel": "email",
    "debug_otp": "123456"  // Only in DEBUG mode
  }
}
```

**Step 2: Verify OTP**

**Endpoint:** `POST /api/v1/auth/otp/verify/`

**Request:**
```json
{
  "channel": "email",
  "code": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": {
    "verified": true
  }
}
```

#### 5. Logout

**Endpoint:** `POST /api/v1/auth/logout/`

**Headers:** 
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": null
}
```

### Role-Based Access Control

#### User Roles

```
citizen      - Regular user, can create posts, report issues, apply for jobs
volunteer    - Can help with community activities
moderator    - Can manage content, status updates, reports
admin        - Full system access
```

#### Permission Examples

```python
# Check user role in code
if request.user.role == UserRole.ADMIN:
    # Admin only action
    pass

# Check permission in views
permission_classes = [
    permissions.IsAuthenticated,
    IsAdminOrModerator(),  # Custom permission
]
```

### Required Headers for Authenticated Requests

```
Authorization: Bearer {access_token}
Content-Type: application/json
```

---

## Core API Endpoints

### Authentication API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | Create new account |
| POST | `/api/v1/auth/login/` | Login with email/password |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token |
| POST | `/api/v1/auth/logout/` | Logout and blacklist token |
| POST | `/api/v1/auth/otp/request/` | Request OTP |
| POST | `/api/v1/auth/otp/verify/` | Verify OTP code |
| GET | `/api/v1/auth/me/` | Get current user |

### Profile API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/profile/me/` | Get user profile |
| PATCH | `/api/v1/profile/me/` | Update user profile |

### OCR Processing API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ocr/process/` | Process image with OCR |
| GET | `/api/v1/ocr/` | List OCR results |
| GET | `/api/v1/ocr/{id}/` | Get OCR result detail |

**OCR Processing Request Example:**

```bash
curl -X POST http://localhost:8000/api/v1/ocr/process/ \
  -H "Authorization: Bearer {token}" \
  -F "image=@/path/to/image.jpg" \
  -F "lat=23.8103" \
  -F "lon=90.4125"
```

### Community Feed API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/community-feed/posts/` | List posts |
| POST | `/api/v1/community-feed/posts/` | Create post |
| GET | `/api/v1/community-feed/posts/{id}/` | Get post detail |
| PATCH | `/api/v1/community-feed/posts/{id}/` | Update post |
| DELETE | `/api/v1/community-feed/posts/{id}/` | Delete post |
| POST | `/api/v1/community-feed/posts/{id}/like/` | Like post |
| POST | `/api/v1/community-feed/posts/{id}/unlike/` | Unlike post |
| GET | `/api/v1/community-feed/comments/` | List comments |
| POST | `/api/v1/community-feed/comments/` | Add comment |
| DELETE | `/api/v1/community-feed/comments/{id}/` | Delete comment |

### Events API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/events-calendar/events/` | List events |
| POST | `/api/v1/events-calendar/events/` | Create event |
| GET | `/api/v1/events-calendar/events/{id}/` | Get event detail |
| PATCH | `/api/v1/events-calendar/events/{id}/` | Update event |
| DELETE | `/api/v1/events-calendar/events/{id}/` | Delete event |
| POST | `/api/v1/events-calendar/events/{id}/rsvp/` | RSVP event |
| POST | `/api/v1/events-calendar/events/{id}/un-rsvp/` | Cancel RSVP |
| GET | `/api/v1/events-calendar/events/my-events/` | Get user's events |

### Blood Donation API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/blood-donation/groups/` | List blood groups |
| GET | `/api/v1/blood-donation/donors/` | List donors |
| POST | `/api/v1/blood-donation/donors/` | Register as donor |
| GET | `/api/v1/blood-donation/requests/` | List requests |
| POST | `/api/v1/blood-donation/requests/` | Create request |
| PATCH | `/api/v1/blood-donation/requests/{id}/` | Update request |

### Issue Reporting API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/report-issues/` | List reports |
| POST | `/api/v1/report-issues/` | Create report |
| GET | `/api/v1/report-issues/{id}/` | Get report detail |
| PATCH | `/api/v1/report-issues/{id}/` | Update report |
| POST | `/api/v1/report-issues/{id}/update-status/` | Update status (admin) |

### Jobs API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/local-jobs/jobs/` | List jobs |
| POST | `/api/v1/local-jobs/jobs/` | Post job |
| GET | `/api/v1/local-jobs/jobs/{id}/` | Get job detail |
| POST | `/api/v1/local-jobs/applications/` | Apply for job |
| GET | `/api/v1/local-jobs/applications/` | List applications |

### Services API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/local-services/categories/` | List categories |
| GET | `/api/v1/local-services/providers/` | List providers |
| POST | `/api/v1/local-services/providers/` | Create provider |
| GET | `/api/v1/local-services/bookings/` | List bookings |
| POST | `/api/v1/local-services/bookings/` | Create booking |

---

## Database Design

### Core Models

#### User (Authentication)
```
- id: UUID (PK)
- email: Email (unique)
- full_name: CharField
- phone: CharField
- role: CharField (choices: admin, moderator, citizen, volunteer)
- is_active: Boolean (default True)
- is_verified: Boolean (default False)
- password: CharField (hashed)
- created_at: DateTime
- updated_at: DateTime
- is_deleted: Boolean (soft delete)
```

#### UserProfile
```
- id: UUID (PK)
- user: OneToOne → User
- location_label: CharField
- push_notifications_enabled: Boolean
- location_services_enabled: Boolean
- posts_count: PositiveInteger (aggregate)
- donations_count: PositiveInteger (aggregate)
- reports_count: PositiveInteger (aggregate)
- created_at: DateTime
- updated_at: DateTime
```

#### Post (Community Feed)
```
- id: UUID (PK)
- author: ForeignKey → User
- category: CharField (choices: news, alert, event)
- content: TextField
- image: ImageField (optional)
- is_published: Boolean
- created_at: DateTime
- updated_at: DateTime
- Indexes: (category, created_at), (is_published)
```

#### PostLike
```
- id: UUID (PK)
- post: ForeignKey → Post
- user: ForeignKey → User
- created_at: DateTime
- Unique: (post, user)
```

#### PostComment
```
- id: UUID (PK)
- post: ForeignKey → Post
- user: ForeignKey → User
- body: TextField
- created_at: DateTime
```

#### Event
```
- id: UUID (PK)
- creator: ForeignKey → User
- title: CharField
- description: TextField
- category: CharField
- venue: CharField
- starts_at: DateTime (indexed)
- ends_at: DateTime
- image: ImageField
- created_at: DateTime
- Indexes: (category, starts_at)
```

#### EventRsvp
```
- id: UUID (PK)
- event: ForeignKey → Event
- user: ForeignKey → User
- created_at: DateTime
- Unique: (event, user)
```

#### OCRProcessingRecord
```
- id: UUID (PK)
- image: ImageField
- latitude: DecimalField
- longitude: DecimalField
- address: TextField
- extracted_text: TextField
- metadata: JSONField
- processing_status: CharField (choices: pending, processing, completed, failed)
- created_at: DateTime
- Indexes: (processing_status, created_at), (latitude, longitude)
```

#### IssueReport
```
- id: UUID (PK)
- reporter: ForeignKey → User
- issue_type: CharField
- status: CharField (choices: pending, in_progress, resolved)
- title: CharField
- description: TextField
- address: CharField
- latitude: DecimalField
- longitude: DecimalField
- photo: ImageField
- created_at: DateTime
- Indexes: (issue_type, status, created_at)
```

#### BloodGroup
```
- id: UUID (PK)
- name: CharField (unique)
```

#### DonorProfile
```
- id: UUID (PK)
- user: OneToOne → User
- blood_group: ForeignKey → BloodGroup
- last_donated_at: DateField
- is_available: Boolean
- latitude: DecimalField
- longitude: DecimalField
```

#### BloodRequest
```
- id: UUID (PK)
- requester: ForeignKey → User
- blood_group: ForeignKey → BloodGroup
- units_needed: PositiveInteger
- urgency: CharField
- status: CharField
- hospital_name: CharField
- required_by: DateTime
- notes: TextField
```

### Relationship Patterns

#### One-to-One
- User ↔ UserProfile
- User ↔ DonorProfile

#### One-to-Many
- User → Posts
- User → Events
- Event → RSVPs
- Post → Comments
- Post → Likes
- User → IssueReports

#### Many-to-Many (via through model)
- Events ↔ Users (via EventRsvp)
- Posts ↔ Users (via PostLike)

### Indexing Strategy

```python
# Primary indexes (automatic on ID)
models.Index(fields=['id'])

# Foreign keys (automatic)
models.Index(fields=['user'])

# Filtering indexes
models.Index(fields=['status', 'created_at'])
models.Index(fields=['category', 'starts_at'])

# Composite indexes for common queries
models.Index(fields=['user', 'is_deleted'])
models.Index(fields=['processing_status', 'created_at'])
```

### Query Optimization

#### Select Related (reduce queries)
```python
queryset = Post.objects.select_related('author').prefetch_related('comments')
```

#### Prefetch Related (batch loading)
```python
queryset = Event.objects.prefetch_related('rsvps').prefetch_related('rsvps__user')
```

#### Only specific fields
```python
queryset = User.objects.only('id', 'email', 'full_name')
```

---

## Services Architecture

### OCR Processing Service

```python
class ProcessingService:
    def __init__(self):
        self.image_service = ImageService()
        self.ocr_service = OCRService()
        self.geocoding_service = GeocodingService()

    @transaction.atomic
    def process_submission(self, image, latitude, longitude):
        # 1. Validate image
        # 2. Create record with PROCESSING status
        # 3. Extract text from image
        # 4. Reverse geocode coordinates
        # 5. Store results
        # 6. Update status to COMPLETED
        # 7. Handle errors appropriately
```

#### Image Service
- Validates file size (max 5MB)
- Validates format (jpg, png, webp)
- Image verification
- Error handling

#### OCR Service
- Image preprocessing (grayscale, contrast)
- Text extraction using pytesseract
- Denoising filter
- Timeout handling (12 seconds)
- Error messages

#### Geocoding Service
- Reverse geocode via Nominatim API
- Caching (24 hours)
- Retry logic (2 attempts)
- Address composition
- Timeout handling (8 seconds)
- Proper User-Agent headers

### Other Services

Each major feature has corresponding services:

- **AuthenticationService**: JWT, OTP, password management
- **ProfileService**: Profile aggregation, stats
- **BloodMatchingService**: Donor-request matching algorithm
- **NotificationService**: Alert aggregation and dispatch

---

## Media Handling

### Upload Configuration

```python
# Settings
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024  # 15MB

# Allowed extensions
OCR_ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
OCR_MAX_IMAGE_SIZE_MB = 5
```

### Upload Paths

```python
# Community feed posts
upload_to="community/posts/%Y/%m/%d/"

# OCR images
upload_to="ocr/uploads/%Y/%m/%d/"

# Reports
upload_to="reports/%Y/%m/%d/"

# Events
upload_to="events/%Y/%m/%d/"
```

### File Security

1. Validate file extension
2. Validate MIME type
3. Validate file size
4. Store outside web root
5. Serve via Django FileResponse
6. Implement rate limiting on uploads

### Multipart Upload Example

```bash
curl -X POST http://localhost:8000/api/v1/ocr/process/ \
  -H "Authorization: Bearer {token}" \
  -F "image=@image.jpg" \
  -F "lat=23.8103" \
  -F "lon=90.4125"
```

---

## Docker Setup

### Docker Compose Services

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"

  web:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - DEBUG=${DEBUG}
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - MYSQL_HOST=db
      - REDIS_URL=redis://redis:6379/0
      - TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
    volumes:
      - .:/app
      - static_volume:/app/static
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000"
```

### Environment Variables

```bash
# Django
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=townflow_db
MYSQL_USER=townflow_user
MYSQL_PASSWORD=secure_password
MYSQL_ROOT_PASSWORD=root_password

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# OCR
OCR_TESSERACT_LANG=eng
OCR_TIMEOUT_SECONDS=12
OCR_MAX_IMAGE_SIZE_MB=5
TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Geocoding
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/reverse
GEOCODING_TIMEOUT_SECONDS=8

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Building and Running

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## Deployment & Operations

### Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure SECURE_SSL_REDIRECT=True
- [ ] Set strong SECRET_KEY
- [ ] Configure database backups
- [ ] Set up log rotation
- [ ] Configure email backend
- [ ] Set up monitoring/alerting
- [ ] Configure rate limiting
- [ ] Set up CDN for media
- [ ] Configure security headers
- [ ] Test error pages
- [ ] Set up status page
- [ ] Configure auto-scaling

### Performance Optimization

#### Database
```python
# Connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 600,  # Connection pool timeout
    }
}

# Query caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

#### API Response
```python
# Pagination
DEFAULT_PAGINATION_CLASS = 'common.pagination.StandardPagination'
PAGE_SIZE = 20

# Throttling
DEFAULT_THROTTLE_RATES = {
    'anon': '60/minute',
    'user': '300/minute',
    'ocr_processing': '30/minute',
}
```

#### Caching Strategy
```python
# Cache expensive queries
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def expensive_view(request):
    pass
```

---

## Development Guide

### Setup Local Environment

```bash
# Clone repository
git clone <repository-url>
cd Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Access
API: http://localhost:8000/api/v1/
Docs: http://localhost:8000/api/docs/swagger/
Admin: http://localhost:8000/admin/
```

### Project Structure

```
Backend/
├── manage.py                  # Django CLI
├── requirements/
│   ├── base.txt              # Common dependencies
│   └── dev.txt               # Development dependencies
├── .env                      # Environment variables (local)
├── docker-compose.yml        # Docker configuration
├── Dockerfile                # Container image
├── conftest.py               # Pytest configuration
└── [other config files]
```

### Common Commands

```bash
# Database
python manage.py migrate                   # Apply migrations
python manage.py makemigrations           # Create migrations
python manage.py sqlmigrate app_name 0001 # Show SQL for migration
python manage.py dbshell                  # Connect to database

# Testing
python manage.py test                     # Run all tests
python manage.py test app_name            # Run app tests
pytest                                    # Run with pytest
pytest -v                                 # Verbose output
pytest --cov=apps                         # With coverage

# Admin
python manage.py createsuperuser          # Create admin user
python manage.py changepassword username  # Change password

# Utilities
python manage.py shell                    # Interactive Python shell
python manage.py flush                    # Reset database
python manage.py collectstatic            # Collect static files
```

---

## Testing

### Test Structure

```
app_name/tests/
├── __init__.py
├── test_serializers.py       # Serializer tests
├── test_views.py             # View/API tests
├── test_services.py          # Service tests
├── test_permissions.py       # Permission tests
├── test_models.py            # Model tests
└── conftest.py               # Pytest fixtures
```

### Writing Tests

#### Model Tests
```python
def test_user_creation():
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        full_name='Test User'
    )
    assert user.email == 'test@example.com'
    assert user.is_verified == False
```

#### Serializer Tests
```python
def test_user_serializer():
    user = User.objects.create_user(
        email='test@example.com',
        full_name='Test User'
    )
    serializer = UserSerializer(user)
    assert serializer.data['email'] == 'test@example.com'
```

#### API Tests
```python
def test_login_api(client):
    User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    response = client.post('/api/v1/auth/login/', {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code == 200
    assert 'access' in response.data['data']
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest apps/authentication/tests/test_views.py

# Specific test
pytest apps/authentication/tests/test_views.py::test_login_api

# With coverage
pytest --cov=apps --cov-report=html

# Watch mode
pytest-watch

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

---

## Troubleshooting

### Common Issues

#### Database Connection Issues

```
Error: Can't connect to MySQL server on 'localhost'

Solution:
1. Ensure MySQL is running: sudo service mysql start
2. Check credentials in .env
3. Verify database exists: mysql -u user -p -e "SHOW DATABASES;"
4. For Docker: docker-compose logs db
```

#### Migration Issues

```
Error: django.db.utils.OperationalError: no such table

Solution:
1. Run migrations: python manage.py migrate
2. For fresh start: python manage.py flush then migrate
3. Check migration file syntax
4. For custom migration: python manage.py makemigrations app_name
```

#### OCR Service Issues

```
Error: pytesseract.TesseractNotFoundError

Solution:
1. Install Tesseract: apt-get install tesseract-ocr
2. Set environment variable: TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
3. For Docker: Already included in Dockerfile
4. Verify installation: tesseract --version
```

#### Geocoding API Issues

```
Error: Nominatim API timeout or rate limit

Solution:
1. Check internet connection
2. Increase timeout: GEOCODING_TIMEOUT_SECONDS=15
3. Implement retry logic (already included)
4. Use cache: Results cached for 24 hours
5. Check User-Agent header compliance
```

#### Authentication Issues

```
Error: Authentication credentials were not provided

Solution:
1. Include Authorization header: Authorization: Bearer {token}
2. Ensure token is valid and not expired
3. Check token in jwt.io for expiration
4. Refresh token if needed
5. Login again if token is blacklisted
```

---

## Scalability & Performance

### Horizontal Scaling

1. **Stateless Application**: Use Redis for session data
2. **Load Balancing**: Distribute traffic with Nginx/HAProxy
3. **Database Sharding**: Partition data by user/region
4. **Caching Layers**: Redis for frequently accessed data
5. **Queue System**: Celery for async tasks

### Vertical Scaling

1. **Increase Resources**: CPU, RAM, Disk
2. **Connection Pooling**: Reduce database connections
3. **Query Optimization**: Use indexes, select_related
4. **Code Optimization**: Profile and optimize slow operations

### Monitoring & Logging

```python
# Application monitoring
- Error tracking: Sentry
- Performance monitoring: New Relic, DataDog
- Log aggregation: ELK Stack, Cloudwatch

# Alerts
- CPU usage > 80%
- Memory usage > 85%
- Error rate > 1%
- Response time > 5s
- Database connection pool exhausted
```

### Rate Limiting

```python
# Configured in settings.py
DEFAULT_THROTTLE_RATES = {
    'anon': '60/minute',        # Anonymous users
    'user': '300/minute',       # Authenticated users
    'ocr_processing': '30/minute',  # Resource-intensive
}
```

### Caching Strategy

```python
# Cache levels
1. Database query cache: QuerySet caching
2. View cache: HTTP response caching
3. Fragment caching: Page component caching
4. Full-page cache: Static page caching

# Implementation
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def list_posts(request):
    pass
```

### Database Optimization

```python
# Indexing
- Primary key (automatic)
- Foreign keys (automatic)
- Filtering fields
- Ordering fields
- Composite indexes for common queries

# Query optimization
- Use select_related for ForeignKey
- Use prefetch_related for reverse relations
- Use only/defer for specific fields
- Batch operations with bulk_create
```

---

## API Response Format

All API responses follow a consistent format:

### Success Response (2xx)

```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "field1": "value1",
    "field2": "value2"
  }
}
```

### Error Response (4xx/5xx)

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {
    "field_name": ["Error message here"],
    "another_field": ["Error message"]
  }
}
```

### Pagination Response

```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": [
    { "id": "..." },
    { "id": "..." }
  ],
  "pagination": {
    "count": 100,
    "next": "http://localhost:8000/api/v1/posts/?page=2",
    "previous": null,
    "page_size": 20,
    "current_page": 1,
    "total_pages": 5
  }
}
```

---

## Curl Examples

### Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "phone": "+8801234567890",
    "role": "citizen"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "{refresh_token}"}'

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{"refresh": "{refresh_token}"}'
```

### Community Feed

```bash
# Create post
curl -X POST http://localhost:8000/api/v1/community-feed/posts/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "news",
    "content": "Check out this amazing event!",
    "is_published": true
  }'

# List posts
curl -X GET "http://localhost:8000/api/v1/community-feed/posts/?category=news&page=1" \
  -H "Authorization: Bearer {access_token}"

# Like post
curl -X POST http://localhost:8000/api/v1/community-feed/posts/{post_id}/like/ \
  -H "Authorization: Bearer {access_token}"
```

### OCR Processing

```bash
# Process image with OCR
curl -X POST http://localhost:8000/api/v1/ocr/process/ \
  -H "Authorization: Bearer {access_token}" \
  -F "image=@/path/to/image.jpg" \
  -F "lat=23.8103" \
  -F "lon=90.4125"

# List OCR results
curl -X GET http://localhost:8000/api/v1/ocr/ \
  -H "Authorization: Bearer {access_token}"
```

### Events

```bash
# Create event
curl -X POST http://localhost:8000/api/v1/events-calendar/events/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Community Cleanup",
    "description": "Let's clean up our neighborhood",
    "category": "festival",
    "venue": "Main Street Park",
    "starts_at": "2026-06-15T09:00:00Z",
    "ends_at": "2026-06-15T12:00:00Z"
  }'

# RSVP event
curl -X POST http://localhost:8000/api/v1/events-calendar/events/{event_id}/rsvp/ \
  -H "Authorization: Bearer {access_token}"
```

---

## Postman Examples

### Import Collection

Create a Postman collection and import these requests:

```json
{
  "info": {
    "name": "TownFlow API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/v1/auth/register/",
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"{{$randomEmail}}\", \"password\": \"SecurePass123!\", \"full_name\": \"Test User\", \"role\": \"citizen\"}"
            }
          }
        }
      ]
    }
  ]
}
```

---

## Additional Resources

- **API Documentation**: http://localhost:8000/api/docs/swagger/
- **Django Documentation**: https://docs.djangoproject.com/
- **DRF Documentation**: https://www.django-rest-framework.org/
- **JWT Documentation**: https://github.com/jpadilla/django-rest-framework-simplejwt

---

*Documentation Last Updated: May 12, 2026*
*Backend Version: 1.0.0*
