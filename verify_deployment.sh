#!/bin/bash
# Production Deployment Verification Script for Namecheap
# Usage: bash verify_deployment.sh

echo "=========================================="
echo "TownFlow Backend - Namecheap Deployment Verification"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
PASSED=0
FAILED=0

# Function to print result
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ $2${NC}"
        ((FAILED++))
    fi
}

# Function to print info
print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

echo "1. Checking Environment Variables..."
echo "======================================"

# Check .env file exists
if [ -f ".env" ]; then
    check_result 0 ".env file exists"
else
    check_result 1 ".env file exists"
fi

# Check DEBUG is False
if grep -q "DEBUG=False" .env; then
    check_result 0 "DEBUG is set to False (production mode)"
else
    check_result 1 "DEBUG should be False (currently True or not set)"
fi

# Check SECRET_KEY
if grep -q "DJANGO_SECRET_KEY=replace_with_secure_secret_key" .env; then
    check_result 1 "DJANGO_SECRET_KEY is still the default (must be changed)"
elif grep -q "DJANGO_SECRET_KEY=" .env; then
    check_result 0 "DJANGO_SECRET_KEY is configured"
else
    check_result 1 "DJANGO_SECRET_KEY is not configured"
fi

# Check ALLOWED_HOSTS
if grep -q "ALLOWED_HOSTS=" .env; then
    HOSTS=$(grep "ALLOWED_HOSTS=" .env | cut -d= -f2)
    if [[ $HOSTS == *"localhost"* ]] && [[ $HOSTS != *","* ]]; then
        check_result 1 "ALLOWED_HOSTS still contains localhost only"
    else
        check_result 0 "ALLOWED_HOSTS is configured"
    fi
else
    check_result 1 "ALLOWED_HOSTS is not configured"
fi

# Check CORS_ALLOWED_ORIGINS
if grep -q "CORS_ALLOWED_ORIGINS=https://" .env; then
    check_result 0 "CORS_ALLOWED_ORIGINS is using HTTPS"
else
    check_result 1 "CORS_ALLOWED_ORIGINS should use HTTPS in production"
fi

# Check CSRF_COOKIE_SECURE
if grep -q "CSRF_COOKIE_SECURE=True" .env; then
    check_result 0 "CSRF_COOKIE_SECURE is enabled"
else
    check_result 1 "CSRF_COOKIE_SECURE should be True"
fi

# Check SESSION_COOKIE_SECURE
if grep -q "SESSION_COOKIE_SECURE=True" .env; then
    check_result 0 "SESSION_COOKIE_SECURE is enabled"
else
    check_result 1 "SESSION_COOKIE_SECURE should be True"
fi

# Check SECURE_SSL_REDIRECT
if grep -q "SECURE_SSL_REDIRECT=True" .env; then
    check_result 0 "SECURE_SSL_REDIRECT is enabled"
else
    check_result 1 "SECURE_SSL_REDIRECT should be True"
fi

echo ""
echo "2. Checking Python Environment..."
echo "=========================================="

# Check Python version
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check_result 0 "Python 3 installed (version: $PY_VERSION)"
else
    check_result 1 "Python 3 is not installed"
fi

# Check virtual environment
if [ -d "venv" ]; then
    check_result 0 "Virtual environment exists"
else
    print_info "Virtual environment not found (create with: python3 -m venv venv)"
fi

# Check Django installation
if python3 -c "import django" 2>/dev/null; then
    check_result 0 "Django is installed"
else
    check_result 1 "Django is not installed"
fi

# Check DRF installation
if python3 -c "import rest_framework" 2>/dev/null; then
    check_result 0 "Django REST Framework is installed"
else
    check_result 1 "Django REST Framework is not installed"
fi

echo ""
echo "3. Checking Django Configuration..."
echo "=========================================="

# Check for migrations
if [ -d "apps/file_manager/migrations" ]; then
    check_result 0 "File manager migrations directory exists"
else
    check_result 1 "File manager migrations directory missing"
fi

# Try to check Django settings
if python3 manage.py check --deploy 2>&1 | grep -q "System check identified no issues"; then
    check_result 0 "Django deployment checks passed"
else
    print_info "Run: python manage.py check --deploy"
fi

echo ""
echo "4. Checking File Permissions..."
echo "=========================================="

# Check if we can write to current directory
if [ -w "." ]; then
    check_result 0 "Directory is writable"
else
    check_result 1 "Directory is not writable"
fi

# Check static directory permissions (if exists)
if [ -d "static" ]; then
    if [ -w "static" ]; then
        check_result 0 "Static directory is writable"
    else
        check_result 1 "Static directory is not writable"
    fi
else
    print_info "Static directory not created yet (will be created with collectstatic)"
fi

# Check media directory permissions (if exists)
if [ -d "media" ]; then
    if [ -w "media" ]; then
        check_result 0 "Media directory is writable"
    else
        check_result 1 "Media directory is not writable"
    fi
else
    print_info "Media directory not created yet"
fi

echo ""
echo "5. Checking Database Configuration..."
echo "=========================================="

# Check database settings in .env
if grep -q "MYSQL_DATABASE=" .env; then
    DB_NAME=$(grep "MYSQL_DATABASE=" .env | cut -d= -f2)
    if [ ! -z "$DB_NAME" ] && [ "$DB_NAME" != "townflow" ]; then
        check_result 0 "Database name configured: $DB_NAME"
    else
        check_result 1 "Database name not properly configured"
    fi
else
    check_result 1 "MYSQL_DATABASE not configured"
fi

# Check database user
if grep -q "MYSQL_USER=" .env; then
    check_result 0 "Database user configured"
else
    check_result 1 "MYSQL_USER not configured"
fi

# Check database password (shouldn't be default)
if grep -q "MYSQL_PASSWORD=replace_db_password" .env; then
    check_result 1 "Database password is still default (must be changed)"
elif grep -q "MYSQL_PASSWORD=" .env; then
    check_result 0 "Database password is configured"
else
    check_result 1 "MYSQL_PASSWORD not configured"
fi

echo ""
echo "6. Checking Security Headers Configuration..."
echo "=========================================="

# Check .htaccess file
if [ -f ".htaccess" ] || [ -f ".htaccess.namecheap" ]; then
    check_result 0 "Apache configuration file exists"
else
    print_info "Copy .htaccess.namecheap to .htaccess for Apache configuration"
fi

# Check if nginx config exists
if [ -f "nginx.conf.namecheap" ]; then
    check_result 0 "Nginx configuration template available"
else
    print_info "Nginx configuration available for VPS setup"
fi

echo ""
echo "7. Recommended Actions..."
echo "=========================================="

echo ""
echo "If you haven't done so already, please:"
echo "1. Run: python manage.py migrate apps.file_manager"
echo "2. Run: python manage.py collectstatic --noinput"
echo "3. Run: python manage.py createsuperuser"
echo "4. Test locally: python manage.py runserver"
echo ""

echo "For Namecheap deployment:"
echo "1. Copy .env.namecheap.example to .env"
echo "2. Update all values for your domain"
echo "3. Copy .htaccess.namecheap to public_html/.htaccess"
echo "4. Follow NAMECHEAP_DEPLOYMENT.md guide"
echo ""

echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your backend is ready for production.${NC}"
    exit 0
else
    echo -e "${RED}✗ Please fix the issues above before deploying to production.${NC}"
    exit 1
fi
