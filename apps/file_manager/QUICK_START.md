# File Manager - Quick Start Guide

## Installation Steps

### 1. Database Migration
First, apply the migrations to create the file manager tables:

```bash
# Local development
python manage.py migrate apps.file_manager

# Docker
docker-compose -f Backend/docker-compose.yml exec web python manage.py migrate
```

### 2. Verify Installation
Check that the file manager app is working:

```bash
# You should see file_manager in installed apps
python manage.py shell
>>> from apps.file_manager.models import UploadedFile
>>> print("File Manager installed successfully!")
```

### 3. Test Upload
Test the file upload endpoint with an authenticated user:

```bash
# Get authentication token
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }'

# Use the token to upload a file
TOKEN="your_access_token_here"
curl -X POST http://localhost:8000/api/v1/file-manager/files/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" \
  -F "title=Test Document" \
  -F "description=My test document" \
  -F "category=document" \
  -F "is_public=false"
```

## Docker Setup

### Using Docker Compose
The file manager is already configured in docker-compose.yml with:
- Media volume for persistent file storage
- Proper environment variables
- CORS and CSRF settings

Start the backend with file manager enabled:

```bash
docker-compose -f Backend/docker-compose.yml up --build
```

### Media Files Location
Inside container: `/app/media/`
Host machine: Maps to your `Backend/media/` directory

## Configuration

### Environment Variables (.env)
```env
# File Upload Limits
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760      # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE=15728640      # 15 MB

# Media Settings
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# Allowed Extensions (in common/validators/files.py)
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
OCR_MAX_IMAGE_SIZE_MB=5
```

### File Size Limits by Category
Edit `apps/file_manager/validators.py` to customize:

```python
FILE_SIZE_LIMITS = {
    "document": 50 * 1024 * 1024,   # 50 MB
    "image": 20 * 1024 * 1024,      # 20 MB
    "video": 500 * 1024 * 1024,     # 500 MB
    "audio": 100 * 1024 * 1024,     # 100 MB
    "archive": 100 * 1024 * 1024,   # 100 MB
    "other": 10 * 1024 * 1024,      # 10 MB
}
```

## Common Tasks

### Upload a File Programmatically

#### Python with Requests
```python
import requests

def upload_file(token, file_path, title, category):
    url = "http://localhost:8000/api/v1/file-manager/files/"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "title": title,
            "category": category,
            "is_public": False
        }
        response = requests.post(url, headers=headers, files=files, data=data)
    
    return response.json()

# Usage
token = "your_token_here"
result = upload_file(token, "document.pdf", "Important Doc", "document")
print(result)
```

#### JavaScript with Fetch
```javascript
async function uploadFile(token, file, title, category) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", title);
  formData.append("category", category);
  formData.append("is_public", false);

  const response = await fetch(
    "http://localhost:8000/api/v1/file-manager/files/",
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    }
  );

  return await response.json();
}

// Usage
const file = document.querySelector('input[type="file"]').files[0];
const result = await uploadFile(token, file, "My Document", "document");
console.log(result);
```

### List Files

```bash
# List all accessible files (paginated)
curl -X GET "http://localhost:8000/api/v1/file-manager/files/?page=1" \
  -H "Authorization: Bearer $TOKEN"

# List only user's files
curl -X GET "http://localhost:8000/api/v1/file-manager/files/my_files/" \
  -H "Authorization: Bearer $TOKEN"

# Filter by category
curl -X GET "http://localhost:8000/api/v1/file-manager/files/?category=document" \
  -H "Authorization: Bearer $TOKEN"
```

### Download a File

```bash
curl -X GET "http://localhost:8000/api/v1/file-manager/files/1/download/" \
  -H "Authorization: Bearer $TOKEN" \
  -o myfile.pdf
```

### Make a File Public

```bash
curl -X PATCH "http://localhost:8000/api/v1/file-manager/files/1/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_public": true}'
```

### Delete a File

```bash
curl -X DELETE "http://localhost:8000/api/v1/file-manager/files/1/" \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### File Upload Fails with "File size exceeds the limit"
- Check file category and size limits in validators.py
- Verify FILE_UPLOAD_MAX_MEMORY_SIZE in .env
- Ensure file isn't corrupted

### Files Not Appearing in Media
- Check MEDIA_ROOT and MEDIA_URL settings
- Verify media directory permissions: `chmod 755 Backend/media/`
- Check docker volume mounts if using Docker

### Permission Denied Errors
- Ensure user is authenticated (has valid token)
- Verify token hasn't expired (default: 30 minutes)
- Check file is public or user is the owner

### Database Errors
- Run: `python manage.py migrate apps.file_manager`
- Check database connection settings in .env

## Monitoring

### Admin Panel
Access file management in Django admin:
- URL: `http://localhost:8000/admin/`
- Navigate to File Manager section
- View all uploaded files and access logs

### Check Storage Usage

```python
from apps.file_manager.services import FileService
from apps.authentication.models import User

user = User.objects.get(username="john_doe")
usage_bytes = FileService.get_file_storage_usage(user)
usage_mb = usage_bytes / (1024 * 1024)
print(f"Storage used: {usage_mb:.2f} MB")
```

## Next Steps

1. **Test with Frontend**: Integrate file upload UI with your frontend
2. **Set File Limits**: Adjust file size limits based on your needs
3. **Configure Backups**: Set up file backup procedures
4. **Monitor Logs**: Regularly check access logs in admin panel
5. **Add Virus Scanning**: Integrate antivirus for uploaded files

For more details, see [FILE_MANAGER_README.md](FILE_MANAGER_README.md)
