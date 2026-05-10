# Project Structure

```text
Backend/
├── apps/
│   ├── alerts/
│   ├── authentication/
│   ├── blood_donation/
│   ├── community_feed/
│   ├── digital_library/
│   ├── events_calendar/
│   ├── home/
│   ├── local_jobs/
│   ├── local_services/
│   ├── onboarding/
│   ├── profile/
│   ├── report_issues/
│   ├── shell/
│   ├── splash/
│   ├── startup/
│   └── volunteer_hub/
├── common/
│   ├── constants/
│   ├── db/
│   ├── exceptions/
│   ├── permissions/
│   ├── responses/
│   ├── storage/
│   ├── validators/
│   ├── filters.py
│   └── pagination.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── v1_urls.py
│   └── wsgi.py
├── requirements/
│   ├── base.txt
│   └── dev.txt
├── docs/
├── media/
├── static/
├── manage.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── API_DOCUMENTATION.md
├── PROJECT_STRUCTURE.md
└── SETUP_GUIDE.md
```

## Responsibility Breakdown
- `apps/`: feature modules aligned with Flutter frontend
- `config/`: global Django config and URL composition
- `common/`: reusable shared primitives (base models, enums, permissions, exceptions, validators)
- `requirements/`: dependency profiles
- `docs/`: additional architecture docs
- `media/`, `static/`: file and static assets

## Core Design Decisions
- UUID IDs for distributed-system-safe records
- Soft delete with managers/querysets
- Time-based audit fields (`created_at`, `updated_at`)
- JWT access/refresh with blacklist for logout
- API versioning (`/api/v1/`) to preserve compatibility
- Centralized enums to maintain frontend-backend contract consistency
