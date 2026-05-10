# TownFlow Backend

Production-ready backend for the TownFlow Flutter application, built with Django, Django REST Framework, MySQL, JWT authentication, Docker, and modular feature apps.

## Tech Stack
- Django 5
- Django REST Framework
- MySQL 8
- JWT auth (`djangorestframework-simplejwt` + blacklist)
- Docker + Docker Compose
- OpenAPI/Swagger (`drf-spectacular`)
- Redis (cache-ready)

## Architecture Highlights
- Modular feature apps mapped 1:1 to frontend modules
- Versioned APIs under `/api/v1/`
- UUID primary keys across domain entities
- Shared base model with timestamps and soft-delete support
- Role-based authorization (`admin`, `moderator`, `citizen`, `volunteer`)
- Centralized exception handling and response envelope pattern
- Throttling, CORS, CSRF, and secure file validation
- Query optimization patterns (`select_related`, `prefetch_related`)

## Database Design (Normalized)
- `authentication_user`: core identity and role table
- `profile_userprofile`: 1:1 profile preferences/statistics extension
- `alerts_alert`: user-scoped notification inbox
- `community_feed_post`, `community_feed_postlike`, `community_feed_postcomment`: feed + engagement
- `events_calendar_event`, `events_calendar_eventrsvp`: event catalog + participation
- `report_issues_issuereport`, `report_issues_issuestatuslog`: complaint lifecycle history
- `blood_donation_bloodgroup`, `blood_donation_donorprofile`, `blood_donation_bloodrequest`, `blood_donation_bloodrequestmatch`
- `local_jobs_job`, `local_jobs_jobapplication`
- `local_services_servicecategory`, `local_services_serviceprovider`, `local_services_servicebooking`
- `digital_library_libraryresource`, `digital_library_resourceprogress`
- `volunteer_hub_volunteerproject`, `volunteer_hub_volunteerenrollment`
- `home_homebanner`, `home_quickaction`, `shell_shellpreference`, `startup_startupprofile`, `onboarding_onboardingprogress`, `splash_apprelease`

All domain tables use UUID keys plus `created_at`/`updated_at`, and include soft-delete columns (`is_deleted`, `deleted_at`) via shared base model.

## Environment Variables
See `.env.example` for full list. High-impact variables:
- App security: `DJANGO_SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- CORS/CSRF: `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
- MySQL: `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`
- JWT/OTP: `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`, `JWT_REFRESH_TOKEN_LIFETIME_DAYS`, `OTP_EXPIRY_MINUTES`
- Runtime: `DJANGO_EXTERNAL_PORT`, `GUNICORN_WORKERS`, `GUNICORN_THREADS`, `GUNICORN_TIMEOUT`

## Feature App Mapping
- alerts
- authentication (auth)
- blood_donation
- community_feed
- digital_library
- events_calendar
- home
- local_jobs
- local_services
- onboarding
- profile
- report_issues
- shell
- splash
- startup
- volunteer_hub

## Quick Start (Docker)
```bash
docker compose up --build
```

Then run in another terminal:
```bash
docker compose exec web python manage.py createsuperuser
```

## Local Run (without Docker)
1. Create and activate Python environment
2. Install dependencies:
```bash
pip install -r requirements/dev.txt
```
3. Configure `.env`
4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Run server:
```bash
python manage.py runserver
```

## API Docs
- Swagger UI: `/api/docs/swagger/`
- ReDoc: `/api/docs/redoc/`
- OpenAPI schema: `/api/schema/`

## Auth Flow (JWT)
1. Register: `POST /api/v1/auth/register/`
2. Login: `POST /api/v1/auth/login/`
3. Refresh token: `POST /api/v1/auth/token/refresh/`
4. Logout + blacklist refresh token: `POST /api/v1/auth/logout/`
5. Current user: `GET /api/v1/auth/me/`

## Commands
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py test
```

## Sample API Testing
### Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "Test User",
    "phone": "01700000000",
    "role": "citizen",
    "password": "StrongPass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "StrongPass123"}'
```

### Create Community Post
```bash
curl -X POST http://localhost:8000/api/v1/community-feed/posts/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"category": "news", "content": "City clean-up starts tomorrow"}'
```

## Required Documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- [SETUP_GUIDE.md](SETUP_GUIDE.md)
- [docs/deploy/namecheap_live_deploy.md](docs/deploy/namecheap_live_deploy.md)

## Production Notes
- Replace all `.env` secret values before deployment
- Restrict CORS/hosts to trusted domains only
- Enable SSL-related secure cookie settings in production
- Add external object storage (S3-compatible) via custom storage backend
- Add CI/CD pipeline for tests, linting, and deployment
- For Namecheap VPS live setup, use `docker-compose.prod.yml` with `.env.production.example`
