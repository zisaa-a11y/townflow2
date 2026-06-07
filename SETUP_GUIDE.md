# TownFlow Backend Setup Guide

This guide covers local setup, Docker deployment, and production configuration for the TownFlow backend.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Setup (Recommended)](#docker-setup-recommended)
4. [Local Development Setup](#local-development-setup)
5. [Database Migrations](#database-migrations)
6. [Running Tests](#running-tests)
7. [Common Commands](#common-commands)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

## Prerequisites

### Docker Setup (Recommended)
- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- 10GB free disk space

### Local Development Setup
- Python 3.12+
- MySQL 8.0+
- Redis 7.2+
- Tesseract OCR (`apt-get install tesseract-ocr`)
- pip or uv package manager

## Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Town/Backend
```

### 2. Create Environment File
```bash
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` and set the following:

```bash
# Django Configuration
DEBUG=False
DJANGO_SECRET_KEY=your-very-secret-key-here-at-least-50-chars
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,http://localhost:3000

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=townetrl_townflow2
MYSQL_USER=townetrl_townflow2user
MYSQL_PASSWORD=FHQHG4A3YPHat7y
MYSQL_ROOT_PASSWORD=root_password_here

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_EXTERNAL_PORT=6379

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
OTP_EXPIRY_MINUTES=10

# OCR Configuration
TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
OCR_TESSERACT_LANG=eng
OCR_TIMEOUT_SECONDS=12
OCR_MAX_IMAGE_SIZE_MB=5

# Geocoding
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/reverse
GEOCODING_TIMEOUT_SECONDS=8

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Django Port
DJANGO_EXTERNAL_PORT=8000
MYSQL_EXTERNAL_PORT=3306

# Gunicorn
GUNICORN_WORKERS=3
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

## Docker Setup (Recommended)

### Quick Start
```bash
# Build and start all services
docker-compose up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Verify
curl http://localhost:8000/api/v1/auth/me/
```

### Service Status
```bash
# View logs
docker-compose logs -f web

# View all services
docker-compose ps

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Database Operations (Docker)
```bash
# Access MySQL
docker-compose exec db mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}

# Backup database
docker-compose exec db mysqldump -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} > backup.sql

# Restore database
docker-compose exec db mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} < backup.sql
```

### Rebuild Images
```bash
# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Force recompilation
docker-compose build --no-cache --pull
```

## Local Development Setup

### 1. Create Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Install development dependencies
pip install -r requirements/dev.txt

# Or specific versions
pip install -r requirements/base.txt
pip install -e .  # For editable install if setup.py exists
```

### 3. Install System Dependencies (Linux/Mac)
```bash
# Ubuntu/Debian
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng \
  default-libmysqlclient-dev python3-dev

# macOS
brew install tesseract mysql

# Check Tesseract installation
tesseract --version
```

### 4. Configure Local Database

#### Option A: Local MySQL
```bash
# Start MySQL
sudo service mysql start  # Linux
brew services start mysql  # macOS

# Create database
mysql -u root -p
CREATE DATABASE townetrl_townflow2 CHARACTER SET utf8mb4;
CREATE USER 'townetrl_townflow2user'@'localhost' IDENTIFIED BY 'FHQHG4A3YPHat7y';
GRANT ALL PRIVILEGES ON townetrl_townflow2.* TO 'townetrl_townflow2user'@'localhost';
FLUSH PRIVILEGES;
```

#### Option B: MySQL Docker Container (no docker-compose)
```bash
docker run -d \
  --name townflow-mysql \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=townetrl_townflow2 \
  -e MYSQL_USER=townetrl_townflow2user \
  -e MYSQL_PASSWORD=FHQHG4A3YPHat7y \
  -p 3306:3306 \
  mysql:8.0
```

### 5. Configure Redis (Local)
```bash
# Start Redis
redis-server

# Or with Docker
docker run -d --name townflow-redis -p 6379:6379 redis:7.2-alpine
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Start Development Server
```bash
python manage.py runserver
# Access at http://localhost:8000
```

## Database Migrations

### Create Migration
```bash
python manage.py makemigrations app_name
python manage.py makemigrations  # All apps
```

### Apply Migrations
```bash
# Apply pending migrations
python manage.py migrate

# Apply specific app
python manage.py migrate app_name

# Apply specific migration number
python manage.py migrate app_name 0005

# See pending migrations
python manage.py showmigrations app_name --plan
```

### Reverse Migration
```bash
# Reverse to previous migration
python manage.py migrate app_name 0004

# Undo all migrations in app
python manage.py migrate app_name zero
```

### SQL Preview
```bash
# See SQL without executing
python manage.py sqlmigrate app_name 0005
```

### Fresh Database (Development Only)
```bash
# WARNING: Deletes all data
python manage.py flush
python manage.py migrate
```

## Running Tests

### Quick Test Run
```bash
# All tests
pytest

# Specific file
pytest apps/authentication/tests/test_views.py

# Specific test
pytest apps/authentication/tests/test_views.py::test_user_login

# Watch mode (auto-rerun on file changes)
pytest-watch
```

### Test Coverage
```bash
# Generate coverage report
pytest --cov=apps --cov=common --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Docker Tests
```bash
docker-compose exec web python manage.py test
docker-compose exec web pytest
```

### Test Organization
```
tests/
├── test_serializers.py       # Serializer validation
├── test_views.py             # API endpoint tests
├── test_services.py          # Business logic tests
├── test_permissions.py       # Permission tests
└── test_models.py            # Model tests
```

## Common Commands

### Django Management
```bash
# Create app
python manage.py startapp app_name

# Run interactive shell
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy

# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Clear cache
python manage.py clear_cache
```

### Database Inspection
```bash
# Connect to Django shell database
python manage.py dbshell

# Inspect model schema
python manage.py sqlmigrate app_name 0001

# Show all migrations
python manage.py showmigrations
```

### API Documentation
```bash
# Generate OpenAPI schema
curl http://localhost:8000/api/schema/

# View Swagger UI
open http://localhost:8000/api/docs/swagger/

# View ReDoc
open http://localhost:8000/api/docs/redoc/
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

### Database Connection Errors
```bash
# Check MySQL is running
service mysql status

# Check connection
mysql -h localhost -u townetrl_townflow2user -p

# Check environment variables
echo $MYSQL_HOST
echo $MYSQL_DATABASE
```

### Tesseract OCR Not Found
```bash
# Install on Ubuntu
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# Install on macOS
brew install tesseract

# Set Tesseract path in .env
TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata
```

### Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping  # Should return PONG

# Check connection
redis-cli

# View all keys
redis-cli keys '*'
```

### Migration Conflicts
```bash
# Merge conflicting migrations
python manage.py makemigrations --merge

# Or show migration history
python manage.py showmigrations
```

## Production Deployment

### Pre-Deployment Checklist
- [ ] DEBUG=False in settings
- [ ] Set strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Test security headers

### Production Environment Variables
```bash
DEBUG=False
DJANGO_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
```

### Deploy with Docker
```bash
# Build production image
docker build -t townflow-backend:latest .

# Run with production settings
docker run -d \
  --env-file .env.production \
  --name townflow-api \
  -p 8000:8000 \
  --restart unless-stopped \
  townflow-backend:latest
```

### Database Backup Strategy
```bash
# Automated daily backup
0 2 * * * mysqldump -u user -p password db > /backups/db-$(date +\%Y\%m\%d).sql

# Recent backup before deployment
mysqldump -u townetrl_townflow2user -p townetrl_townflow2 > backup-$(date +%Y%m%d-%H%M%S).sql
```

### Performance Optimization
```python
# Database connection pooling
# Update requirements
pip install django-connection-pool

# Configure connection pool
DATABASES = {
    'default': {
        'ENGINE': 'django_mysql.connection_pool',
        'POOL_SIZE': 10,
        'MAX_OVERFLOW': 5,
    }
}
```

---

## Getting Help

- **API Documentation**: http://localhost:8000/api/docs/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **Project Docs**: See `Backend/docs/api.md`
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/

## Next Steps

1. Review the [API Documentation](docs/api.md)
2. Check [Project Structure](PROJECT_STRUCTURE.md)
3. Run tests: `pytest`
4. Start developing!

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
