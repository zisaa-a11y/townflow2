# Namecheap Backend Deployment Guide

## 📋 Prerequisites

- Namecheap Shared Hosting or VPS account
- cPanel access
- Domain pointing to your Namecheap server
- SSH access (for advanced setup)
- Python 3.9+ installed on your hosting

## 🚀 Step 1: Prepare Your Domain

1. **Update Allowed Hosts** in `.env`:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **Update CORS** in `.env`:
```env
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

3. **Update Frontend URL** in `.env`:
```env
APP_FRONTEND_BASE_URL=https://yourdomain.com
```

## 🗄️ Step 2: Set Up Database

### Via cPanel (Easiest for Shared Hosting):

1. Login to cPanel
2. Go to **MySQL Databases**
3. Create a new database:
   - Database name: `username_townflow`
   - Username: `username_townuser`
   - Password: Strong password
   - Add all privileges

4. Update `.env`:
```env
MYSQL_DATABASE=username_townflow
MYSQL_USER=username_townuser
MYSQL_PASSWORD=your-strong-password
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### For Remote MySQL (if needed):
```env
MYSQL_HOST=mysql.yourdomain.com
MYSQL_PORT=3306
```

## 📁 Step 3: Set Up File Structure

1. **Create directories via cPanel File Manager or SSH**:
```bash
cd /home/username
mkdir -p public_html/static
mkdir -p public_html/media
mkdir -p logs
mkdir -p town_backend
chmod 755 public_html/static
chmod 755 public_html/media
chmod 755 logs
```

2. **Update `.env` with correct paths**:
```env
STATIC_ROOT=/home/username/public_html/static
STATIC_URL=/static/
MEDIA_ROOT=/home/username/public_html/media
MEDIA_URL=/media/
LOG_FILE_PATH=/home/username/logs/django.log
```

## 📦 Step 4: Upload Code

### Option A: Using Git (Recommended)
```bash
cd /home/username
git clone https://github.com/zisaa-a11y/town_flow.git
cd town_flow/Backend
```

### Option B: Using SFTP
1. Upload entire Backend directory to `/home/username/town_backend/`
2. Via cPanel File Manager or FileZilla

## 🔧 Step 5: Set Up Python Environment

### Via cPanel Setup Python App (for Shared Hosting):

1. Go to **Setup Python App** in cPanel
2. Create new application:
   - Python version: 3.9 or 3.10
   - App root: `/home/username/town_backend`
   - App startup file: `config/wsgi.py`
   - App URI: `/api/`

This will create a virtual environment automatically.

### Via SSH (Alternative):
```bash
cd /home/username/town_backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements/base.txt
```

## ⚙️ Step 6: Configure Environment Variables

1. Copy `.env.namecheap.example` to `.env`:
```bash
cp .env.namecheap.example .env
```

2. Edit `.env` with actual values:
```env
DEBUG=False
DJANGO_SECRET_KEY=your-super-secure-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MYSQL_DATABASE=username_townflow
MYSQL_USER=username_townuser
MYSQL_PASSWORD=your-password
```

## 🗄️ Step 7: Run Database Migrations

```bash
cd /home/username/town_backend
source venv/bin/activate
python manage.py migrate
python manage.py migrate apps.file_manager
python manage.py collectstatic --noinput
```

## 👤 Step 8: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow prompts:
- Email: admin@yourdomain.com
- Password: Strong password
- Confirm password

## 🔐 Step 9: Configure SSL Certificate

1. **In cPanel - AutoSSL** (Usually free):
   - Go to **AutoSSL** in cPanel
   - Enable for your domain
   - Wait for certificate to issue (usually automatic)

2. **Force HTTPS**: Update `.env`:
```env
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 🌐 Step 10: Set Up Web Server (cPanel)

### If using cPanel Python setup:
The setup is mostly automatic. Configure addon domain if needed.

### If using shared hosting with .htaccess:

1. Create `/home/username/public_html/.htaccess`:
```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /

    # Redirect all requests to /api/ to the Django app
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^api/(.*)$ /api/$1 [L]
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "DENY"
    Header set X-XSS-Protection "1; mode=block"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
```

## 📊 Step 11: Create Cache Table (if using database cache)

```bash
python manage.py createcachetable
```

## 🧪 Step 12: Test API

```bash
# Check admin panel
curl -k https://yourdomain.com/admin/

# Check API documentation
curl -k https://yourdomain.com/api/schema/

# Get authentication token
curl -X POST https://yourdomain.com/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "your-password"
  }'
```

## 📈 Step 13: Set Up Cron Jobs (Optional)

For periodic tasks, add to cPanel **Cron Jobs**:

```bash
# Clean up old tokens (daily at 2 AM)
0 2 * * * cd /home/username/town_backend && source venv/bin/activate && python manage.py flushexpiredtokens

# Clean up sessions (weekly)
0 3 * * 0 cd /home/username/town_backend && source venv/bin/activate && python manage.py clearsessions
```

## 📝 Step 14: Set Up Logging

1. Create logs directory (already done in Step 3)
2. Verify logs are working:
```bash
tail -f /home/username/logs/django.log
```

## 🔍 Verification Checklist

- [x] Domain pointing to Namecheap servers
- [x] Database created and accessible
- [x] Python environment installed
- [x] Code uploaded and configured
- [x] `.env` file with production settings
- [x] Migrations completed successfully
- [x] Static files collected
- [x] SSL certificate installed
- [x] API endpoints responding
- [x] Admin panel accessible
- [x] Authentication working
- [x] File uploads working

## 🆘 Troubleshooting

### 500 Internal Server Error

1. **Check logs**:
```bash
tail -f /home/username/logs/django.log
```

2. **Common causes**:
   - Database connection failed
   - Missing SECRET_KEY
   - Wrong file permissions
   - Missing Python packages

### Database Connection Error

```bash
# Test MySQL connection
mysql -u username_townuser -p -h localhost username_townflow

# If fails, verify:
# 1. Username and password in .env
# 2. Database exists
# 3. User has privileges
```

### Static Files Not Loading

```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
chmod -R 755 /home/username/public_html/static
```

### CORS/CSRF Errors

1. **Check ALLOWED_HOSTS** in `.env`:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

2. **Check CORS origins**:
```env
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

3. **Check CSRF trusted origins**:
```env
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Memory/Timeout Issues

1. **Increase memory in .env**:
```env
FILE_UPLOAD_MAX_MEMORY_SIZE=20971520  # 20MB
DATA_UPLOAD_MAX_MEMORY_SIZE=31457280  # 30MB
```

2. **Increase timeout**:
```env
GUNICORN_TIMEOUT=240  # 4 minutes
```

## 🚀 Optimization Tips

### For Better Performance:

1. **Enable Gzip compression** in Apache:
```apache
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml application/json
</IfModule>
```

2. **Enable browser caching**:
```apache
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType application/json "access plus 1 hour"
    ExpiresByType image/* "access plus 1 year"
</IfModule>
```

3. **Optimize database**:
```bash
# Update statistics (monthly)
python manage.py dbshell
> ANALYZE TABLE authentication_user;
> ANALYZE TABLE file_manager_uploadedfile;
```

## 📊 Monitoring

### Check Server Stats:
```bash
# Disk usage
du -sh /home/username/town_backend
du -sh /home/username/public_html/media

# Memory usage
free -h

# Running processes
ps aux | grep python
```

### Monitor Logs:
```bash
# Real-time logs
tail -f /home/username/logs/django.log

# Error logs
grep ERROR /home/username/logs/django.log
```

## 🔄 Deployment Automation

Create a deployment script `/home/username/deploy.sh`:

```bash
#!/bin/bash
cd /home/username/town_backend
source venv/bin/activate

# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements/base.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application (if using cPanel Python)
touch /home/username/town_backend/config/wsgi.py

echo "Deployment completed!"
```

Make executable:
```bash
chmod +x /home/username/deploy.sh
```

## 📞 Support Resources

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Namecheap Support: https://www.namecheap.com/support/

## ✅ Deployment Complete!

Your TownFlow backend is now running on Namecheap! 🎉

**Next steps:**
1. Test all API endpoints
2. Set up your frontend to connect to https://yourdomain.com/api/
3. Configure CDN for media files (optional)
4. Set up automated backups
