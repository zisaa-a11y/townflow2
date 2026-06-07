# Namecheap Deployment Guide (`api.townflow.org`)

This guide is for deploying the Django backend on Namecheap cPanel Python App.

## 1. DNS Setup (Namecheap)

Create an `A` record:

- Host: `api`
- Value: your hosting server IP
- TTL: Automatic

If `townflow.org` is already active, keep the root domain records unchanged and only add the `api` subdomain record.

## 2. Prepare cPanel Python App

In cPanel:

1. Open **Setup Python App**.
2. Create app with:
- Python version: `3.11` or `3.12` (match your package compatibility)
- Application root: `api.townflow.org`
- Application URL: `api.townflow.org`
- Application startup file: `passenger_wsgi.py`
3. Note the virtualenv path shown by cPanel.

## 3. Upload Project

Upload all backend files into the app root (`api.townflow.org`).

Required key files in app root:

- `manage.py`
- `passenger_wsgi.py`
- `.env`
- `requirements.txt`
- `config/`
- `apps/`
- `common/`

## 4. Install Dependencies

From cPanel Terminal (inside app root):

```bash
pip install -r requirements.txt
```

## 5. Create Production `.env`

Use the template file:

```bash
cp .env.namecheap.example .env
```

Then update at minimum:

- `DJANGO_SECRET_KEY`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `STATIC_ROOT`
- `MEDIA_ROOT`

For your domain, keep:

- `ALLOWED_HOSTS=api.townflow.org,townflow.org,www.townflow.org`
- `CSRF_TRUSTED_ORIGINS=https://api.townflow.org,https://townflow.org,https://www.townflow.org`
- `CORS_ALLOWED_ORIGINS=https://townflow.org,https://www.townflow.org`

## 6. Database and Cache Table

Run migrations:

```bash
python manage.py migrate
```

Create DB cache table (required when `CACHE_BACKEND=db`):

```bash
python manage.py createcachetable django_cache_table
```

Create admin user:

```bash
python manage.py createsuperuser
```

## 7. Static and Media

Collect static files:

```bash
python manage.py collectstatic --noinput
```

Make sure the directories in `.env` exist and are writable:

- `STATIC_ROOT`
- `MEDIA_ROOT`

## 8. Passenger Restart

After env/config changes, restart the app from cPanel Python App panel.

If needed from terminal:

```bash
touch tmp/restart.txt
```

## 9. Verify Deployment

Check:

- `https://api.townflow.org/api/schema/`
- `https://api.townflow.org/api/docs/swagger/`
- `https://api.townflow.org/admin/`

Security check:

```bash
python manage.py check --deploy
```

## 10. Common Namecheap Notes

- Shared hosting usually does not provide Redis. Use `CACHE_BACKEND=db`.
- Keep `DEBUG=False` in production.
- Do not commit `.env`.
- Use cPanel MySQL credentials, not local credentials.
- If OCR fails, keep `OCR_TESSERACT_CMD` empty unless Namecheap confirms Tesseract path.
