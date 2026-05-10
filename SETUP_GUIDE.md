# Setup Guide

## 1. Prerequisites
- Docker + Docker Compose
- Or Python 3.12+, MySQL 8, Redis (for local non-docker setup)

## 2. Environment Configuration
Copy and edit env values:
```bash
cp .env.example .env
```

Important variables:
- `DJANGO_SECRET_KEY`
- `MYSQL_*`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- JWT lifetimes and throttle rates

## 3. Run with Docker
```bash
docker compose up --build
```

### Docker-Only Workflow (Recommended)
If you use Docker as the source of truth, do not rely on host virtual environments for backend commands.

From workspace root (`Town`):
```bash
docker compose -f Backend/docker-compose.yml up --build -d
docker compose -f Backend/docker-compose.yml exec web python manage.py migrate
docker compose -f Backend/docker-compose.yml exec web python manage.py test
docker compose -f Backend/docker-compose.yml logs -f web
```

From backend root (`Town/Backend`):
```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
docker compose logs -f web
```

### Migration Commands
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### Superuser Command
```bash
docker compose exec web python manage.py createsuperuser
```

## 4. Run without Docker
```bash
python -m venv .venv
# activate virtualenv
pip install -r requirements/dev.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 5. API Verification
- Health check by opening Swagger: `http://localhost:8000/api/docs/swagger/`
- Acquire JWT from login endpoint and hit protected routes

## 6. Deployment Steps
1. Set `DEBUG=False`
2. Use secure secrets and rotate keys
3. Set strict `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS`
4. Enable `SECURE_SSL_REDIRECT`, secure cookies
5. Use managed MySQL and Redis
6. Run migrations in release phase
7. Serve media/static using object storage + CDN if needed
8. Configure process supervision and health checks
9. Enable log shipping (ELK/CloudWatch/Grafana stack)

## 7. Scaling Strategy
- Horizontal scale app containers behind load balancer
- Add read replicas for high read loads
- Cache frequently read endpoints with Redis
- Introduce task queue workers (Celery) for async jobs (notifications, media processing)
- Add DB indexes based on real query plans and APM traces

## 8. Security Checklist
- Validate all uploads (`jpg/jpeg/png/webp`, size-limited)
- Avoid raw SQL in application code
- Keep dependencies updated and scan for vulnerabilities
- Rate-limit auth endpoints and sensitive write APIs
- Enforce least privilege for DB and infra credentials

## 9. Sample .env
Use `.env.example` as template. Keep `.env` secrets out of VCS.

## 10. API Testing Examples
### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"StrongPass123"}'
```

### Get Profile
```bash
curl http://localhost:8000/api/v1/profile/me/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Create Issue Report
```bash
curl -X POST http://localhost:8000/api/v1/report-issues/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_type":"road",
    "title":"Pothole on Main Road",
    "description":"Large pothole near market",
    "address":"Sector 10"
  }'
```
