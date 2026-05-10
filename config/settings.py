import os
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_filters",
    "apps.authentication",
    "apps.alerts",
    "apps.blood_donation",
    "apps.community_feed",
    "apps.digital_library",
    "apps.events_calendar",
    "apps.home",
    "apps.local_jobs",
    "apps.local_services",
    "apps.onboarding",
    "apps.ocr_processing",
    "apps.profile",
    "apps.report_issues",
    "apps.shell",
    "apps.splash",
    "apps.startup",
    "apps.volunteer_hub",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

mysql_options = {
    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    "charset": "utf8mb4",
}

mysql_ssl_ca = env("MYSQL_SSL_CA", default="")
mysql_ssl_cert = env("MYSQL_SSL_CERT", default="")
mysql_ssl_key = env("MYSQL_SSL_KEY", default="")

if mysql_ssl_ca or mysql_ssl_cert or mysql_ssl_key:
    mysql_options["ssl"] = {}
    if mysql_ssl_ca:
        mysql_options["ssl"]["ca"] = mysql_ssl_ca
    if mysql_ssl_cert:
        mysql_options["ssl"]["cert"] = mysql_ssl_cert
    if mysql_ssl_key:
        mysql_options["ssl"]["key"] = mysql_ssl_key

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MYSQL_DATABASE"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_PASSWORD"),
        "HOST": env("MYSQL_HOST"),
        "PORT": env("MYSQL_PORT"),
        "CONN_MAX_AGE": env.int("MYSQL_CONN_MAX_AGE", default=60),
        "OPTIONS": mysql_options,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = env("STATIC_ROOT", default=str(BASE_DIR / "static"))
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_ROOT = env("MEDIA_ROOT", default=str(BASE_DIR / "media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "authentication.User"
SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "common.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": env("THROTTLE_ANON_RATE", default="60/minute"),
        "user": env("THROTTLE_USER_RATE", default="300/minute"),
        "ocr_processing": env("THROTTLE_OCR_PROCESSING_RATE", default="30/minute"),
    },
    "EXCEPTION_HANDLER": "common.exceptions.handler.custom_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=30)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": env("API_TITLE", default="TownFlow API"),
    "DESCRIPTION": env("API_DESCRIPTION", default="Enterprise backend API for TownFlow"),
    "VERSION": env("API_VERSION", default="1.0.0"),
    "SERVE_INCLUDE_SCHEMA": False,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://redis:6379/1"),
    }
}

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = env("SECURE_REFERRER_POLICY", default="same-origin")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST", default=False)

if not DEBUG:
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(message)s",
        },
        "simple": {
            "format": "%(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("LOG_LEVEL", default="INFO"),
            "propagate": False,
        }
    },
}

APP_FRONTEND_BASE_URL = env("APP_FRONTEND_BASE_URL", default="")
OTP_EXPIRY_MINUTES = env.int("OTP_EXPIRY_MINUTES", default=10)

OCR_ALLOWED_IMAGE_EXTENSIONS = set(
    ext.lower() for ext in env.list("OCR_ALLOWED_IMAGE_EXTENSIONS", default=["jpg", "jpeg", "png", "webp"])
)
OCR_MAX_IMAGE_SIZE_MB = env.int("OCR_MAX_IMAGE_SIZE_MB", default=5)
OCR_TIMEOUT_SECONDS = env.int("OCR_TIMEOUT_SECONDS", default=12)
OCR_TESSERACT_LANG = env("OCR_TESSERACT_LANG", default="eng")
OCR_TESSERACT_CONFIG = env("OCR_TESSERACT_CONFIG", default="--oem 3 --psm 6")
OCR_APPLY_DENOISE = env.bool("OCR_APPLY_DENOISE", default=True)
OCR_TESSERACT_CMD = env("OCR_TESSERACT_CMD", default="")

NOMINATIM_BASE_URL = env("NOMINATIM_BASE_URL", default="https://nominatim.openstreetmap.org/reverse")
NOMINATIM_USER_AGENT = env("NOMINATIM_USER_AGENT", default="townflow-backend/1.0")
NOMINATIM_REFERER = env("NOMINATIM_REFERER", default="http://localhost")
GEOCODING_TIMEOUT_SECONDS = env.int("GEOCODING_TIMEOUT_SECONDS", default=8)
GEOCODING_RETRY_TOTAL = env.int("GEOCODING_RETRY_TOTAL", default=2)
GEOCODING_RETRY_BACKOFF = env.float("GEOCODING_RETRY_BACKOFF", default=0.5)
GEOCODING_ACCEPT_LANGUAGE = env("GEOCODING_ACCEPT_LANGUAGE", default="en")

FILE_UPLOAD_MAX_MEMORY_SIZE = env.int("FILE_UPLOAD_MAX_MEMORY_SIZE", default=10 * 1024 * 1024)
DATA_UPLOAD_MAX_MEMORY_SIZE = env.int("DATA_UPLOAD_MAX_MEMORY_SIZE", default=15 * 1024 * 1024)
