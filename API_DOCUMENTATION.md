# API Documentation - TownFlow Backend

Base URL: `/api/v1/`

Authentication: `Authorization: Bearer <access_token>`

## Response Pattern
Success:
```json
{
  "success": true,
  "message": "Request processed successfully.",
  "data": {}
}
```

Error:
```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {}
}
```

## Authentication
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/token/refresh/`
- `POST /auth/logout/`
- `GET /auth/me/`

## Alerts
- `GET /alerts/`
- `POST /alerts/`
- `PATCH /alerts/{id}/`
- `POST /alerts/mark-all-read/`
- `POST /alerts/{id}/mark-read/`

## Blood Donation
- `GET /blood-donation/groups/`
- `GET|POST /blood-donation/donors/`
- `GET|POST /blood-donation/requests/`

Enums:
- urgency: `normal`, `urgent`
- status: `pending`, `matched`, `fulfilled`

## Community Feed
- `GET|POST /community-feed/posts/`
- `POST /community-feed/posts/{id}/like/`
- `POST /community-feed/posts/{id}/unlike/`
- `GET|POST /community-feed/comments/`

Enums:
- category: `news`, `alert`, `event`

## Digital Library
- `GET|POST /digital-library/resources/`
- `GET|POST /digital-library/progress/`

Enums:
- category: `book`, `article`, `video`

## Events Calendar
- `GET|POST /events-calendar/events/`
- `POST /events-calendar/events/{id}/rsvp/`
- `POST /events-calendar/events/{id}/un-rsvp/`
- `GET /events-calendar/events/my-events/`

Enums:
- category: `festival`, `workshop`, `sports`, `cultural`

## Home
- `GET /home/config/`

## Local Jobs
- `GET|POST /local-jobs/jobs/`
- `GET|POST /local-jobs/applications/`

Enums:
- job_type: `fullTime`, `partTime`, `remote`

## Local Services
- `GET /local-services/categories/`
- `GET|POST /local-services/providers/`
- `GET|POST /local-services/bookings/`

## Onboarding
- `GET|PATCH /onboarding/progress/`

## OCR Processing
- `POST /ocr/process/`

Content type:
- `multipart/form-data`

Request fields:
- `image` (png/jpg/jpeg/webp)
- `lat`
- `lon`

Sample success payload:
```json
{
  "success": true,
  "message": "Image processed successfully",
  "data": {
    "id": "33d4c87f-7dc7-41fc-a16f-0f6f6962537d",
    "latitude": 23.0,
    "longitude": 90.0,
    "address": "Dhaka, Bangladesh",
    "extracted_text": "Sample OCR text",
    "image_url": "http://localhost:8000/media/ocr-processing/2026/05/10/sample.jpg",
    "created_at": "2026-05-10T10:00:00Z"
  }
}
```

## Profile
- `GET|PATCH /profile/me/`

## Report Issues
- `GET|POST /report-issues/`
- `POST /report-issues/{id}/update-status/`

Enums:
- issue_type: `road`, `water`, `electricity`, `waste`, `other`
- status: `pending`, `inProgress`, `resolved`

## Shell
- `GET|PATCH /shell/preferences/`

## Splash
- `GET /splash/releases/`

## Startup
- `GET|PATCH /startup/profile/`

## Volunteer Hub
- `GET|POST /volunteer-hub/projects/`
- `GET /volunteer-hub/projects/my-volunteering/`
- `GET|POST /volunteer-hub/enrollments/`

Enums:
- status: `upcoming`, `active`, `completed`

## Pagination
Default pagination is page-based.
- query params: `page`, `page_size`
- max `page_size`: `200`

## Filtering, Search, Ordering
Endpoints expose `filterset_fields`, `search_fields`, and `ordering_fields` as configured in each ViewSet.

## OpenAPI
- `/api/schema/`
- `/api/docs/swagger/`
- `/api/docs/redoc/`
