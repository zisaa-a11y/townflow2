# OCR + Reverse Geocoding Integration Guide

## 1. Feature Overview
This document describes the production-oriented integration of OCR and reverse geocoding into the TownFlow backend.

Feature capability:
- Accepts image + latitude + longitude from authenticated API clients.
- Extracts text from image using Tesseract OCR.
- Resolves coordinates into a human-readable address via OpenStreetMap Nominatim.
- Stores request input and processing outputs in MySQL.
- Returns standardized API response payloads.

Primary endpoint:
- `POST /api/v1/ocr/process/`

---

## 2. Architecture Summary
The integration is implemented as a dedicated Django app with service-layer orchestration:

- App: `apps.ocr_processing`
- Pattern: `APIView -> Serializer -> ProcessingService -> (ImageService + OCRService + GeocodingService) -> Model`
- Persistence: `OCRProcessingRecord` table with UUID PK, timestamps, soft-delete fields via shared `BaseModel`.
- API versioning: Mounted under existing `api/v1` router.

Key design characteristics:
- Reusable service classes for OCR, geocoding, image validation.
- Environment-driven behavior (timeouts, retries, OCR options, headers).
- Centralized response envelope alignment with existing backend patterns.
- Request throttling scope for abuse control.

---

## 3. Folder Structure
Implemented structure:

```text
apps/ocr_processing/
├── __init__.py
├── admin.py
├── apps.py
├── urls.py
├── constants/
│   ├── __init__.py
│   └── processing.py
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py
│   └── 0002_alter_ocrprocessingrecord_image.py
├── models/
│   ├── __init__.py
│   └── ocr_record.py
├── permissions/
│   ├── __init__.py
│   └── ocr_permissions.py
├── serializers/
│   ├── __init__.py
│   └── process_serializer.py
├── services/
│   ├── __init__.py
│   ├── geocoding_service.py
│   ├── image_service.py
│   ├── ocr_service.py
│   └── processing_service.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_geocoding_service.py
│   ├── test_ocr_service.py
│   ├── test_serializers.py
│   └── test_validators.py
├── utils/
│   ├── __init__.py
│   └── file_naming.py
├── validators/
│   ├── __init__.py
│   ├── coordinates.py
│   └── image.py
└── views/
    ├── __init__.py
    └── process_view.py
```

---

## 4. OCR Workflow
1. Client uploads multipart form data (`image`, `lat`, `lon`).
2. `OCRProcessingCreateSerializer` validates input shape.
3. `ImageService` performs image safety checks:
   - extension allow-list
   - max size
   - image integrity verification
4. `OCRService` processes image:
   - grayscale conversion
   - autocontrast
   - optional denoise (median filter)
   - `pytesseract.image_to_string` with timeout
   - text cleanup (trim and normalize lines)
5. `ProcessingService` persists output and status transitions.

Timeout handling:
- OCR timeout is environment-driven (`OCR_TIMEOUT_SECONDS`).
- Runtime OCR exceptions are normalized into service errors.

---

## 5. Reverse Geocoding Workflow
1. `GeocodingService` builds Nominatim request payload from `lat/lon`.
2. Uses a dedicated `requests.Session` with retry adapter.
3. Applies production-safe headers:
   - `User-Agent`
   - `Referer`
   - `Accept`
   - `Accept-Language`
4. Parses structured response:
   - `display_name`
   - normalized `address_line`
   - `components`
   - raw provider payload for traceability

Retry and timeout configuration is environment-driven:
- `GEOCODING_TIMEOUT_SECONDS`
- `GEOCODING_RETRY_TOTAL`
- `GEOCODING_RETRY_BACKOFF`

---

## 6. Service Layer Responsibilities
### image_service.py
- Validate file existence
- Validate file size
- Validate extension
- Verify image integrity with Pillow

### ocr_service.py
- Preprocess image (grayscale + optional denoise)
- OCR extraction using pytesseract
- Cleanup OCR output text
- Handle OCR-specific exceptions and timeouts

### geocoding_service.py
- Reverse geocode via Nominatim endpoint
- Request timeout and retry-safe behavior
- Provider error handling
- Structured address parsing

### processing_service.py
- Orchestrate complete workflow
- Persist processing state transitions (`processing`, `completed`, `failed`)
- Persist extracted text and resolved address
- Store geocoding metadata payload

---

## 7. Database Schema
Model: `OCRProcessingRecord`

Fields:
- `id` (UUID PK)
- `image` (ImageField, secure upload path)
- `latitude` (Decimal(9,6), indexed)
- `longitude` (Decimal(9,6), indexed)
- `address` (TextField)
- `extracted_text` (TextField)
- `metadata` (JSONField)
- `processing_status` (pending/processing/completed/failed, indexed)
- `created_at`, `updated_at`
- Soft delete fields inherited: `is_deleted`, `deleted_at`

Indexes:
- `(processing_status, created_at)`
- `(latitude, longitude)`

---

## 8. API Endpoint Contract
### Endpoint
- `POST /api/v1/ocr/process/`

### Auth
- JWT Bearer token required.

### Content-Type
- `multipart/form-data`

### Request Fields
- `image`: file (`png`, `jpg`, `jpeg`, `webp`)
- `lat`: decimal latitude (`-90` to `90`)
- `lon`: decimal longitude (`-180` to `180`)

### Success Response (201)
```json
{
  "success": true,
  "message": "Image processed successfully",
  "data": {
    "id": "33d4c87f-7dc7-41fc-a16f-0f6f6962537d",
    "latitude": 23.0,
    "longitude": 90.0,
    "address": "Dhaka, Bangladesh",
    "extracted_text": "Detected text...",
    "image_url": "http://localhost:8000/media/ocr-processing/2026/05/10/file.jpg",
    "created_at": "2026-05-10T10:00:00Z"
  }
}
```

### Error Response (400)
```json
{
  "success": false,
  "message": "Processing failed",
  "errors": {
    "detail": ["Reverse geocoding provider is temporarily unavailable."]
  }
}
```

---

## 9. Swagger / OpenAPI
Endpoint schema is exposed at:
- `/api/schema/`
- `/api/docs/swagger/`
- `/api/docs/redoc/`

`OCRProcessAPIView` includes:
- Request schema
- Success response schema
- Failure response schema
- Request and response examples

---

## 10. Dependencies Added
Updated `requirements/base.txt`:
- `pytesseract==0.3.13`
- `requests==2.32.3`

---

## 11. Docker Changes
### Dockerfile updates
Installed OCR runtime dependencies:
- `tesseract-ocr`
- `tesseract-ocr-eng`
- `libjpeg62-turbo-dev`
- `zlib1g-dev`
- `libwebp-dev`

### docker-compose updates
Web service environment includes:
- `TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata`

---

## 12. Settings and Environment Variables
### Settings updates
- Added app to `INSTALLED_APPS`
- Added OCR throttle scope rate: `ocr_processing`
- Added upload memory limit settings
- Added OCR and geocoding config settings

### Environment variables
```env
THROTTLE_OCR_PROCESSING_RATE=30/minute

OCR_ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
OCR_MAX_IMAGE_SIZE_MB=5
OCR_TIMEOUT_SECONDS=12
OCR_TESSERACT_LANG=eng
OCR_TESSERACT_CONFIG=--oem 3 --psm 6
OCR_APPLY_DENOISE=True
OCR_TESSERACT_CMD=

NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/reverse
NOMINATIM_USER_AGENT=townflow-backend/1.0
NOMINATIM_REFERER=http://localhost
GEOCODING_TIMEOUT_SECONDS=8
GEOCODING_RETRY_TOTAL=2
GEOCODING_RETRY_BACKOFF=0.5
GEOCODING_ACCEPT_LANGUAGE=en

FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
DATA_UPLOAD_MAX_MEMORY_SIZE=15728640
```

---

## 13. Media Configuration
Already configured in settings:
- `MEDIA_URL`
- `MEDIA_ROOT`

Upload path behavior:
- Files stored under date-partitioned folders:
  - `media/ocr-processing/YYYY/MM/DD/<uuid>.<ext>`

This improves organization and reduces collision risk.

---

## 14. Security Considerations
Implemented controls:
- JWT authentication required.
- Request throttling with OCR-specific scope.
- Coordinate range validation.
- File extension + content validation.
- Upload size limits.
- Exception-safe processing (service-layer error normalization).
- ORM-based persistence (SQL injection-safe data access path).

Operational guidance:
- Keep `NOMINATIM_USER_AGENT` and `NOMINATIM_REFERER` set correctly in production.
- Tune throttle and timeout settings based on traffic profile.

---

## 15. Migration Commands
Run from backend root:

```bash
python manage.py makemigrations ocr_processing
python manage.py migrate
```

Generated migrations:
- `0001_initial.py`
- `0002_alter_ocrprocessingrecord_image.py`

---

## 16. Docker Commands
```bash
docker compose build --no-cache web
docker compose up -d
docker compose logs -f web
```

Optional one-off migration inside container:
```bash
docker compose exec web python manage.py migrate
```

---

## 17. Setup Instructions
1. Ensure `.env` contains all OCR/geocoding variables.
2. Install dependencies (`pip install -r requirements/base.txt`) or build Docker image.
3. Run migrations.
4. Start backend service.
5. Verify `/api/docs/swagger/` includes OCR Processing tag and endpoint.

---

## 18. Run Instructions
Local:
```bash
python manage.py runserver
```

Docker:
```bash
docker compose up --build
```

---

## 19. Testing Instructions
Run app-level tests:

```bash
python manage.py test apps.ocr_processing.tests
```

Test coverage includes:
- Serializer validation tests
- API response contract tests
- OCR service tests (mocked Tesseract)
- Geocoding service tests (mocked HTTP)
- Coordinate validator tests

---

## 20. cURL Examples
```bash
curl -X POST "http://localhost:8000/api/v1/ocr/process/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/absolute/path/to/image.jpg" \
  -F "lat=23.810331" \
  -F "lon=90.412521"
```

Failure case example (invalid lat):
```bash
curl -X POST "http://localhost:8000/api/v1/ocr/process/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/absolute/path/to/image.jpg" \
  -F "lat=130.000000" \
  -F "lon=90.412521"
```

---

## 21. Postman Example
### Request
- Method: `POST`
- URL: `http://localhost:8000/api/v1/ocr/process/`
- Auth: Bearer Token (`<ACCESS_TOKEN>`)
- Body: `form-data`
  - `image` (type: File)
  - `lat` (type: Text, sample `23.810331`)
  - `lon` (type: Text, sample `90.412521`)

### Example Postman Collection Item JSON (partial)
```json
{
  "name": "OCR Process",
  "request": {
    "method": "POST",
    "header": [
      { "key": "Authorization", "value": "Bearer {{access_token}}" }
    ],
    "url": {
      "raw": "{{base_url}}/api/v1/ocr/process/",
      "host": ["{{base_url}}"],
      "path": ["api", "v1", "ocr", "process", ""]
    },
    "body": {
      "mode": "formdata",
      "formdata": [
        { "key": "image", "type": "file", "src": "/path/to/image.jpg" },
        { "key": "lat", "type": "text", "value": "23.810331" },
        { "key": "lon", "type": "text", "value": "90.412521" }
      ]
    }
  }
}
```

---

## 22. Scalability Notes
- OCR and geocoding logic is service-based and independently replaceable.
- Provider configs are environment-driven for multi-environment portability.
- Status field allows future async/offline processing migration (Celery/RQ).
- Metadata JSON allows schema-safe enrichment without table redesign.
- Scoped throttling controls heavy endpoint abuse.

---

## 23. Production Recommendations
- Move OCR processing to async workers for high-volume workloads.
- Add circuit breaker/cache for geocoding provider to reduce external API dependence.
- Add explicit observability (latency metrics, error rates per provider).
- Store uploaded images in object storage (S3-compatible) via custom storage backend.
- Add service-level tracing for OCR and geocoding spans.
- Enforce stricter WAF/file scanning if handling untrusted public uploads.
