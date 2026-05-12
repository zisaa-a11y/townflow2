# File Manager Documentation

## Overview
The File Manager is a comprehensive file upload and management system for the TownFlow backend. It allows users to upload, manage, and share files with proper access control and logging.

## Features

- **File Upload**: Upload files with automatic size and type validation
- **File Organization**: Categorize files (document, image, video, audio, archive, other)
- **Access Control**: Public/private file sharing with permission management
- **Access Logging**: Track all file access, downloads, and modifications
- **Storage Management**: Monitor file storage usage per user
- **File Metadata**: Automatic file size and MIME type detection

## API Endpoints

### Files Management

#### List All Files (paginated)
```
GET /api/v1/file-manager/files/
```
Returns paginated list of user's own files and all public files.

**Query Parameters:**
- `category`: Filter by file category (document, image, video, audio, archive, other)
- `is_public`: Filter by public/private (true/false)
- `uploaded_by`: Filter by uploader username
- `search`: Search in title and description
- `ordering`: Sort by created_at or download_count

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/v1/file-manager/files/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "file": "/media/uploads/1/document/example.pdf",
      "file_url": "http://localhost:8000/media/uploads/1/document/example.pdf",
      "title": "Example PDF",
      "description": "Sample PDF document",
      "category": "document",
      "file_size": 1024000,
      "file_type": "application/pdf",
      "uploaded_by": 1,
      "uploaded_by_username": "john_doe",
      "is_public": true,
      "download_count": 5,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Upload a File
```
POST /api/v1/file-manager/files/
```
Upload a new file with automatic validation.

**Request (multipart/form-data):**
```
file: <binary file>
title: "My Document"
description: "This is my document"
category: "document"
is_public: true
```

**Response (201 Created):**
```json
{
  "id": 2,
  "file": "/media/uploads/1/document/mydoc.pdf",
  "file_url": "http://localhost:8000/media/uploads/1/document/mydoc.pdf",
  "title": "My Document",
  "description": "This is my document",
  "category": "document",
  "file_size": 2048000,
  "file_type": "application/pdf",
  "uploaded_by": 1,
  "uploaded_by_username": "john_doe",
  "is_public": true,
  "download_count": 0,
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Get File Details
```
GET /api/v1/file-manager/files/{id}/
```
Get detailed information about a specific file.

#### Update File
```
PUT /api/v1/file-manager/files/{id}/
PATCH /api/v1/file-manager/files/{id}/
```
Update file metadata (title, description, is_public). Only file owner can update.

#### Delete File
```
DELETE /api/v1/file-manager/files/{id}/
```
Delete a file. Only file owner can delete.

#### Download File
```
GET /api/v1/file-manager/files/{id}/download/
```
Download a file and log the access. Returns download URL or redirects to file.

**Response:**
```json
{
  "message": "Download counted",
  "file_url": "http://localhost:8000/media/uploads/1/document/example.pdf"
}
```

#### Get User's Files
```
GET /api/v1/file-manager/files/my_files/
```
Get all files uploaded by the authenticated user.

#### Get Public Files
```
GET /api/v1/file-manager/files/public_files/
```
Get all public files from all users.

#### Get File Access Logs
```
GET /api/v1/file-manager/files/{id}/access_logs/
```
Get access logs for a file. Only file owner can view.

**Response:**
```json
[
  {
    "id": 1,
    "file": 1,
    "file_title": "Example PDF",
    "accessed_by": 2,
    "accessed_by_username": "jane_doe",
    "action": "download",
    "ip_address": "192.168.1.1",
    "created_at": "2024-01-15T10:35:00Z"
  }
]
```

## File Categories & Limits

| Category | Max Size | Allowed Types |
|----------|----------|---------------|
| document | 50 MB | PDF, DOC, DOCX, XLS, XLSX, TXT, CSV |
| image | 20 MB | JPG, PNG, GIF, WebP, SVG |
| video | 500 MB | MP4, MPEG, MOV, AVI, WebM |
| audio | 100 MB | MP3, WAV, OGG, WebM, AAC |
| archive | 100 MB | ZIP, RAR, 7Z, GZIP |
| other | 10 MB | Any other files |

## Permission System

- **IsAuthenticated**: Required for all file operations
- **IsFileOwnerOrReadOnly**: Users can read public files or their own files; only owners can edit/delete
- **IsFileOwner**: Only file owners can access certain operations

## Error Handling

### 400 Bad Request
```json
{
  "file": ["File size exceeds the limit for document files."]
}
```

### 403 Forbidden
```json
{
  "error": "You don't have permission to download this file."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Examples

### Upload a Document using cURL
```bash
curl -X POST http://localhost:8000/api/v1/file-manager/files/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  -F "description=Important document" \
  -F "category=document" \
  -F "is_public=false"
```

### Upload an Image using Python
```python
import requests

url = "http://localhost:8000/api/v1/file-manager/files/"
headers = {"Authorization": f"Bearer {token}"}

with open("image.jpg", "rb") as f:
    files = {"file": f}
    data = {
        "title": "My Image",
        "description": "Beautiful image",
        "category": "image",
        "is_public": True
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    print(response.json())
```

### List User's Files
```bash
curl -X GET "http://localhost:8000/api/v1/file-manager/files/my_files/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Download a File
```bash
curl -X GET "http://localhost:8000/api/v1/file-manager/files/1/download/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o downloaded_file.pdf
```

## Environment Variables

```env
# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE=15728640  # 15 MB
MEDIA_URL=/media/
MEDIA_ROOT=/app/media
```

## File Storage

Files are stored in the following structure:
```
media/
  uploads/
    {user_id}/
      {category}/
        {filename}
```

Example: `media/uploads/1/document/example.pdf`

## Access Logging

All file accesses are logged with:
- File ID
- User who accessed it
- Action (view, download, delete)
- IP address
- Timestamp

## Integration with Docker

The file manager works seamlessly with Docker:
- Files are persisted in Docker volumes
- Media folder is mounted from the host
- All environment variables are configurable

## Testing

Run tests with:
```bash
python manage.py test apps.file_manager
```

## Future Enhancements

- Virus scanning for uploaded files
- File preview/thumbnail generation
- Advanced search with filters
- File sharing with specific users
- File versioning
- Backup and recovery system
