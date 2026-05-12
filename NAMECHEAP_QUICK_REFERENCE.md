# Namecheap Production Setup - Quick Reference

## 🔐 Essential Configuration Changes

### 1. Update Django Settings (.env)

```bash
# Security
DEBUG=False
DJANGO_SECRET_KEY=generate-new-secure-key-here

# Domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
APP_FRONTEND_BASE_URL=https://yourdomain.com

# HTTPS/Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
USE_X_FORWARDED_HOST=True

# Database (Namecheap cPanel MySQL)
MYSQL_DATABASE=username_dbname
MYSQL_USER=username_user
MYSQL_PASSWORD=strong-password
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Files & Storage
STATIC_ROOT=/home/username/public_html/static
STATIC_URL=/static/
MEDIA_ROOT=/home/username/public_html/media
MEDIA_URL=/media/

# Logging
LOG_FILE_PATH=/home/username/logs/django.log
LOG_LEVEL=WARNING

# Cache (use database cache for shared hosting)
CACHE_BACKEND=database
```

---

## 🚀 One-Time Setup Commands

```bash
# 1. SSH into Namecheap
ssh username@yourdomain.com

# 2. Navigate to project
cd /home/username/town_backend

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements/base.txt

# 5. Run migrations
python manage.py migrate
python manage.py migrate apps.file_manager

# 6. Create cache table
python manage.py createcachetable

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Create superuser
python manage.py createsuperuser

# 9. Check for errors
python manage.py check --deploy

# 10. Test locally
python manage.py runserver 127.0.0.1:8000
```

---

## 📝 Environment Variables Summary

| Variable | Example | Purpose |
|----------|---------|---------|
| DEBUG | False | Disable debug mode in production |
| DJANGO_SECRET_KEY | abc123... | Secret key for Django |
| ALLOWED_HOSTS | yourdomain.com | Allowed domains |
| CORS_ALLOWED_ORIGINS | https://yourdomain.com | CORS allowed domains |
| MYSQL_DATABASE | username_db | Database name |
| MYSQL_USER | username_user | Database user |
| MYSQL_PASSWORD | strong-pass | Database password |
| STATIC_ROOT | /home/username/public_html/static | Static files path |
| MEDIA_ROOT | /home/username/public_html/media | Media files path |
| SECURE_SSL_REDIRECT | True | Force HTTPS |

---

## 🗂️ Directory Structure

```
/home/username/
├── public_html/
│   ├── static/              # CSS, JS, images
│   ├── media/               # User uploads
│   ├── .htaccess            # Apache config
│   └── index.html           # Frontend (optional)
├── town_backend/            # Django project
│   ├── Backend/
│   ├── Frontend/
│   ├── venv/                # Python environment
│   └── .env                 # Environment variables
└── logs/
    └── django.log           # Error logs
```

---

## 🔄 Deployment Workflow

### Initial Deployment
```
1. Upload code → 2. Create .env → 3. Install packages 
→ 4. Run migrations → 5. Collect static 
→ 6. Create superuser → 7. Test
```

### Update Deployment
```
1. Pull latest code → 2. Install new packages 
→ 3. Run migrations → 4. Collect static 
→ 5. Restart app
```

---

## ✅ Production Checklist

- [ ] DEBUG=False in .env
- [ ] DJANGO_SECRET_KEY is strong and unique
- [ ] ALLOWED_HOSTS has correct domain
- [ ] CORS/CSRF properly configured
- [ ] SSL certificate installed
- [ ] Database created and connected
- [ ] Static files collected
- [ ] Media directory writable
- [ ] Logs directory created
- [ ] Superuser created
- [ ] API endpoints responding
- [ ] Admin panel accessible at /admin/
- [ ] HTTPS working
- [ ] No DEBUG errors in logs

---

## 🆘 Troubleshooting Quick Fixes

### 500 Error
```bash
# Check logs
tail -f /home/username/logs/django.log

# Run diagnostics
python manage.py check --deploy
```

### Database Connection Failed
```bash
# Test MySQL connection
mysql -u username_user -p -h localhost username_db

# Verify credentials in .env
cat .env | grep MYSQL_
```

### Static Files Missing
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Set permissions
chmod -R 755 /home/username/public_html/static
```

### CORS Errors
```bash
# Update .env
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 🔐 Security Checklist

- [ ] HTTPS enabled (SSL certificate)
- [ ] DEBUG=False
- [ ] SECRET_KEY is random and strong
- [ ] ALLOWED_HOSTS restricted to your domain
- [ ] Database password is strong
- [ ] .env file is not accessible publicly
- [ ] Security headers configured (.htaccess)
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] SQL injection protection active

---

## 📊 Performance Optimization

### In .env:
```env
# Cache settings
CACHE_BACKEND=redis  # or database for shared hosting

# Rate limiting
THROTTLE_ANON_RATE=100/hour
THROTTLE_USER_RATE=500/hour

# File upload
FILE_UPLOAD_MAX_MEMORY_SIZE=20971520  # 20MB
DATA_UPLOAD_MAX_MEMORY_SIZE=31457280  # 30MB
```

### In Apache (.htaccess):
```apache
# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain
</IfModule>

# Browser caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/* "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
</IfModule>
```

---

## 📈 Monitoring Commands

```bash
# Check disk usage
du -sh /home/username/town_backend
du -sh /home/username/public_html/media

# Check recent errors
tail -n 50 /home/username/logs/django.log | grep ERROR

# Check database size
mysql -u username_user -p -e "SELECT table_name, 
  ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb 
  FROM information_schema.tables WHERE table_schema = 'username_db';"

# Monitor API response
watch -n 5 'tail -n 20 /home/username/logs/django.log'
```

---

## 🔄 Regular Maintenance

### Weekly
- [ ] Check error logs
- [ ] Monitor disk usage
- [ ] Verify backups

### Monthly
- [ ] Clean old logs
- [ ] Review security headers
- [ ] Update dependencies (if safe)
- [ ] Database optimization

### Quarterly
- [ ] Security audit
- [ ] Performance review
- [ ] Backup verification

---

## 📞 Helpful Links

- **Namecheap cPanel**: https://www.namecheap.com/support/knowledgebase/
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Let's Encrypt**: https://letsencrypt.org/docs/
- **MySQL Documentation**: https://dev.mysql.com/doc/

---

## 🚀 Example Deployment Script

Create `/home/username/deploy.sh`:

```bash
#!/bin/bash
set -e

PROJECT_DIR="/home/username/town_backend"
cd $PROJECT_DIR

echo "Pulling latest code..."
git pull origin main

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements/base.txt

echo "Running migrations..."
python manage.py migrate
python manage.py migrate apps.file_manager

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Deployment complete!"
```

Make executable:
```bash
chmod +x /home/username/deploy.sh
```

Run deployment:
```bash
/home/username/deploy.sh
```

---

## 🎯 Success Indicators

✅ API responds to requests  
✅ Admin panel accessible at /admin/  
✅ Authentication working  
✅ File uploads functional  
✅ HTTPS enabled  
✅ No 500 errors in logs  
✅ Static files loading  
✅ Database accessible  

---

**Status**: Ready for Production Deployment 🚀
