# Namecheap Deployment Architecture

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Internet / Users                        │
│                                                              │
│  HTTPS://yourdomain.com                                     │
│  HTTPS://www.yourdomain.com                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │    Namecheap Nameservers       │
        │   (DNS Resolution)             │
        │                                │
        │  A Record → Namecheap IP       │
        └────────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │   SSL Certificate (AutoSSL)    │
        │   (HTTPS Encryption)           │
        └────────────────┬───────────────┘
                         │
                         ▼
    ┌────────────────────────────────────────┐
    │      Namecheap Server / cPanel         │
    │                                        │
    │  /home/username/                       │
    │  ├── public_html/                      │
    │  │   ├── .htaccess ◄─ Security Config │
    │  │   ├── static/    ◄─ CSS, JS, etc  │
    │  │   └── media/     ◄─ User uploads   │
    │  │                                    │
    │  ├── town_backend/                    │
    │  │   ├── Backend/   ◄─ Django code   │
    │  │   ├── venv/      ◄─ Python env    │
    │  │   └── .env       ◄─ Config        │
    │  │                                    │
    │  └── logs/                            │
    │      └── django.log ◄─ Error logs    │
    │                                        │
    └────────────┬───────────────────────────┘
                 │
        ┌────────┴────────────┐
        │                     │
        ▼                     ▼
   ┌─────────────┐      ┌──────────────┐
   │   Apache    │      │    MySQL     │
   │  / Nginx    │      │  (cPanel)    │
   │             │      │              │
   │ • .htaccess │      │ • Database   │
   │ • Routing   │      │ • Tables     │
   │ • Headers   │      │ • Backups    │
   └──────┬──────┘      └──────────────┘
          │
          ▼
   ┌──────────────────────────┐
   │   Django Application     │
   │   (config/wsgi.py)       │
   │                          │
   │  • Authentication        │
   │  • File Management       │
   │  • API Endpoints         │
   │  • File Uploads/Downloads│
   └──────────────────────────┘
```

---

## 📊 Request Flow

```
User Request (HTTPS)
    │
    ▼
Namecheap Firewall
    │
    ▼
SSL Decryption
    │
    ▼
Apache/.htaccess
    ├─ Check HTTPS redirect ─────────────────────┐
    ├─ Apply security headers                    │
    ├─ Check CORS                                │
    └─ Route to application                      │
                                                 │
    ┌────────────────────────────────────────────┘
    │
    ▼
Django Application
    ├─ Authentication (JWT)
    ├─ Route to viewset
    ├─ Check permissions
    ├─ Process request
    └─ Query database
                │
                ▼
            MySQL Database
                │
                ▼
            Return data
                │
                ▼
    Response with JSON/File
                │
                ▼
            Apply Cache
                │
                ▼
    HTTPS Response to Client
```

---

## 🔐 Security Layers

```
┌──────────────────────────────────────────┐
│         Layer 1: HTTPS/SSL                │
│  • Encrypted transmission                 │
│  • Certificate validation                 │
└──────────────────────────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│    Layer 2: Firewall/Rate Limiting        │
│  • Blocks malicious IPs                   │
│  • Rate limiting on endpoints             │
│  • DDoS protection                        │
└──────────────────────────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│    Layer 3: Apache/Nginx (.htaccess)      │
│  • Security headers                       │
│  • CORS validation                        │
│  • Static file serving                    │
│  • Blocks sensitive files                 │
└──────────────────────────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│   Layer 4: Django Middleware              │
│  • CSRF protection                        │
│  • Authentication checks                  │
│  • Permission validation                  │
│  • Request sanitization                   │
└──────────────────────────────────────────┘
                    ▼
┌──────────────────────────────────────────┐
│    Layer 5: Application Logic             │
│  • Business rules                         │
│  • Data validation                        │
│  • Database operations                    │
│  • File operations                        │
└──────────────────────────────────────────┘
```

---

## 📁 Directory Structure (Namecheap)

```
/home/username/
│
├── public_html/                     ◄─ Web root (document root)
│   ├── .htaccess                    ◄─ Apache configuration
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── media/
│   │   └── uploads/
│   │       └── {user_id}/
│   │           ├── document/
│   │           ├── image/
│   │           ├── video/
│   │           └── audio/
│   └── index.html                   ◄─ Optional: redirect to API
│
├── town_backend/                    ◄─ Django project
│   ├── Backend/                     ◄─ Django app directory
│   │   ├── config/
│   │   │   ├── settings.py         ◄─ Production settings
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── v1_urls.py
│   │   ├── apps/
│   │   │   ├── authentication/
│   │   │   ├── file_manager/
│   │   │   └── ... (other apps)
│   │   ├── common/
│   │   ├── manage.py
│   │   └── requirements/
│   │       └── base.txt
│   │
│   ├── venv/                        ◄─ Python virtual environment
│   │   ├── bin/
│   │   ├── lib/
│   │   └── include/
│   │
│   └── .env                         ◄─ Production environment variables
│
├── logs/                            ◄─ Application logs
│   ├── django.log                   ◄─ Django error log
│   └── access.log                   ◄─ Apache access log
│
└── backups/                         ◄─ Database backups (optional)
    ├── database_20240115.sql
    └── database_20240122.sql
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────┐
│    Frontend Application         │
│  (React/Flutter/Web)            │
│                                 │
│  • User Interface               │
│  • API Calls                    │
│  • File Operations              │
└────────────────┬────────────────┘
                 │
                 │ HTTP/S Request
                 │ (JSON + Files)
                 ▼
        ┌────────────────────┐
        │  Django REST API   │
        │  (Django App)      │
        │                    │
        │  • Authentication  │
        │  • Serializers     │
        │  • Validators      │
        │  • Permissions     │
        └────────┬───────────┘
                 │
        ┌────────┴──────────┐
        │                   │
        ▼                   ▼
   ┌─────────────┐   ┌──────────────┐
   │   Models    │   │   Services   │
   │             │   │              │
   │ • User      │   │ • Business   │
   │ • File      │   │   logic      │
   │ • Upload    │   │ • File ops   │
   │ • Log       │   │ • Auth       │
   └──────┬──────┘   └──────────────┘
          │
          │ Database Queries
          │ + File Operations
          ▼
   ┌──────────────────────┐
   │   MySQL Database     │
   │                      │
   │ • Users table        │
   │ • Files table        │
   │ • Logs table         │
   │ • Sessions table     │
   └──────────────────────┘
          │
          │ Query Results
          │
          ▼
   ┌──────────────────────┐
   │   Response JSON      │
   │  + Files (if needed) │
   └──────────────────────┘
          │
          │ HTTP/S Response
          │
          ▼
   ┌─────────────────────┐
   │  Frontend App       │
   │                    │
   │  Display Data      │
   │  Update UI         │
   │  Show Files        │
   └─────────────────────┘
```

---

## ⚙️ Configuration Stack

```
┌──────────────────────────────────────┐
│   Environment Configuration           │
│   (.env file)                         │
│                                       │
│  • DEBUG=False                        │
│  • ALLOWED_HOSTS                      │
│  • Database credentials               │
│  • API settings                       │
│  • Security settings                  │
└──────────────────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│   Django Settings Module              │
│   (config/settings.py)                │
│                                       │
│  • Read .env variables                │
│  • Configure apps                     │
│  • Setup database                     │
│  • Configure cache                    │
│  • Setup logging                      │
└──────────────────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│   WSGI Application                    │
│   (config/wsgi.py)                    │
│                                       │
│  • Initialize Django                  │
│  • Apply middleware                   │
│  • Ready for requests                 │
└──────────────────────────────────────┘
           ▼
┌──────────────────────────────────────┐
│   Web Server                          │
│   (Apache / Nginx)                    │
│                                       │
│  • Handles HTTP/HTTPS                 │
│  • Routes requests                    │
│  • Serves static files                │
│  • Manages connections                │
└──────────────────────────────────────┘
```

---

## 📊 Database Schema (Simplified)

```
┌──────────────────────────────┐
│    authentication_user       │
├──────────────────────────────┤
│ id (PK)                      │
│ email                        │
│ username                     │
│ password_hash                │
│ is_active                    │
│ created_at                   │
│ updated_at                   │
└──────────────────────────────┘
           │
           │ 1:N
           │
┌──────────────────────────────┐
│   file_manager_uploadedfile  │
├──────────────────────────────┤
│ id (PK)                      │
│ file (path)                  │
│ title                        │
│ category                     │
│ file_size                    │
│ uploaded_by_id (FK) ────────┐
│ is_public                    │
│ download_count               │
│ created_at                   │
└──────────────────────────────┘
           │
           │ 1:N
           │
┌──────────────────────────────┐
│  file_manager_fileaccesslog  │
├──────────────────────────────┤
│ id (PK)                      │
│ file_id (FK)                 │
│ accessed_by_id (FK)          │
│ action                       │
│ ip_address                   │
│ created_at                   │
└──────────────────────────────┘
```

---

## 🔄 CI/CD Workflow (Recommended)

```
┌──────────────┐
│  Git Commit  │
│  to Main     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  GitHub Actions      │
│                      │
│  • Run tests         │
│  • Check lint        │
│  • Verify build      │
└──────┬───────────────┘
       │ (if passes)
       ▼
┌──────────────────────┐
│  Deploy to           │
│  Namecheap           │
│                      │
│  • SSH pull code     │
│  • Run migrations    │
│  • Collect static    │
│  • Restart app       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Smoke Tests         │
│                      │
│  • API responds      │
│  • DB connected      │
│  • Files accessible  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Monitor Logs        │
│                      │
│  • Check errors      │
│  • Verify responses  │
│  • Alert on issues   │
└──────────────────────┘
```

---

## 📈 Performance Architecture

```
User Request
    │
    ▼
┌──────────────────┐
│ Nginx/Apache     │
│ • Gzip compress  │
│ • Cache static   │
│ • Rate limiting  │
└────────┬─────────┘
         │ (from cache)
         ├──────────────────────────┐
         │                          │
         ▼ (if needed)              ▼ (to cache)
    ┌──────────────┐         ┌──────────────────┐
    │   Django     │────────→│  Cache Layer     │
    │   Application│         │  (Redis/DB)      │
    └──────┬───────┘         └──────────────────┘
           │
           ▼
    ┌──────────────┐
    │   Database   │
    │  (Optimized) │
    └──────────────┘
```

---

## ✅ Deployment Stages

```
Development
    ↓
  .env (DEBUG=True)
    ↓
Testing
    ↓
  .env.namecheap (DEBUG=False)
    ↓
Staging (Optional)
    ↓
  .env.production (Final)
    ↓
Production
    ↓
  Namecheap Server
    ↓
  Users Access via HTTPS
```

---

## 🎯 Key Success Metrics

```
Performance
├── API Response Time < 500ms
├── File Upload Speed > 1MB/s
└── Database Query Time < 100ms

Availability
├── Uptime > 99.5%
├── Error Rate < 0.1%
└── Cache Hit Rate > 70%

Security
├── 0 SQL Injections
├── 0 XSS Attacks
└── SSL Grade A

Users
├── Successful Logins
├── File Uploads Complete
└── Satisfied Experience
```

---

This architecture is production-ready and designed specifically for Namecheap hosting! 🚀
