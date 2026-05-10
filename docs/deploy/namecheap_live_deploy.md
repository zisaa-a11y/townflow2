# Namecheap Live Deployment Guide (Docker + External MySQL)

## Scope
This guide makes TownFlow backend live on a Namecheap VPS using Docker Compose and an external MySQL database.

## 1. Infrastructure Requirements
- Namecheap VPS (Ubuntu 22.04+ recommended)
- Domain/subdomain (example: `api.yourdomain.com`) pointing to VPS IP
- MySQL database credentials (Namecheap managed MySQL or remote MySQL host)
- Open ports: 80, 443, and backend mapped port (or use reverse proxy)

## 2. Server Bootstrap
```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Log out and log in again to apply docker group permission.

## 3. Deploy Source
```bash
git clone <your-repo-url> town
cd town/Backend
```

## 4. Production Environment
Create production env from template:
```bash
cp .env.production.example .env
```

Edit `.env` and set at minimum:
- `DEBUG=False`
- `DJANGO_SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`
- `MYSQL_HOST`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_PORT`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

## 5. Bring Up Production Stack
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Verify services:
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web
```

## 6. DNS and Reverse Proxy
Point `api.yourdomain.com` A record to VPS IP in Namecheap DNS.

Use Nginx (host-level or container-level) to terminate TLS and proxy to `localhost:8000`.

Minimal proxy target:
- upstream: `127.0.0.1:8000`
- include headers: `X-Forwarded-For`, `X-Forwarded-Proto`, `Host`

## 7. Database Readiness
Ensure external MySQL allows VPS IP access.

Run app migrations:
```bash
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

Create superuser:
```bash
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## 8. Smoke Tests
- Swagger: `https://api.yourdomain.com/api/docs/swagger/`
- Schema: `https://api.yourdomain.com/api/schema/`

Health checks from logs:
```bash
docker compose -f docker-compose.prod.yml logs -f web
```

## 9. Update and Rollout
```bash
git pull
docker compose -f docker-compose.prod.yml up --build -d
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## 10. Security Checklist
- `DEBUG=False`
- Strong secrets and rotated DB credentials
- Strict CORS/CSRF origins
- TLS enabled for domain
- Database network access restricted to VPS IP
- Regular image and dependency patching
