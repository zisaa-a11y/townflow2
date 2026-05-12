# File Manager Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Application                      │
│                    (React/Flutter App)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Django Backend                              │
├─────────────────────────────────────────────────────────────┤
│  API Layer                                                   │
│  ├─ UploadedFileViewSet (views.py)                          │
│  │  ├─ POST /files/ - Upload                               │
│  │  ├─ GET /files/ - List                                   │
│  │  ├─ GET /files/{id}/ - Detail                           │
│  │  ├─ PUT/PATCH /files/{id}/ - Update                     │
│  │  ├─ DELETE /files/{id}/ - Delete                        │
│  │  ├─ GET /files/{id}/download/ - Download               │
│  │  └─ GET /files/{id}/access_logs/ - Logs                │
│  └─ Authentication & Permissions                           │
│     ├─ IsFileOwnerOrReadOnly                               │
│     └─ IsFileOwner                                          │
├─────────────────────────────────────────────────────────────┤
│  Serializers (serializers.py)                               │
│  ├─ UploadedFileSerializer - Full representation           │
│  ├─ FileUploadSerializer - Upload form with validation     │
│  └─ FileAccessLogSerializer - Log representation           │
├─────────────────────────────────────────────────────────────┤
│  Business Logic                                             │
│  ├─ FileService (services.py) - High-level operations     │
│  ├─ UploadedFileRepository (repositories.py)              │
│  ├─ FileAccessLogRepository (repositories.py)             │
│  └─ Validators (validators.py) - File validation          │
├─────────────────────────────────────────────────────────────┤
│  Models (models.py)                                        │
│  ├─ UploadedFile                                           │
│  │  ├─ file (FileField)                                   │
│  │  ├─ title, description                                 │
│  │  ├─ category                                           │
│  │  ├─ file_size, file_type                               │
│  │  ├─ uploaded_by (ForeignKey to User)                  │
│  │  └─ is_public, download_count                         │
│  └─ FileAccessLog                                          │
│     ├─ file (ForeignKey to UploadedFile)                 │
│     ├─ accessed_by (ForeignKey to User)                  │
│     ├─ action (view/download/delete)                     │
│     └─ ip_address                                         │
├─────────────────────────────────────────────────────────────┤
│  Data Access Layer                                          │
│  ├─ Django ORM                                             │
│  └─ QuerySet optimization with select_related()           │
└─────────────────┬────────────────┬──────────────────────────┘
                  │                │
                  │                │
        ┌─────────▼──┐      ┌──────▼──────┐
        │  Database  │      │  File Store │
        │  (MySQL)   │      │  (/media/)  │
        │            │      │             │
        │ • Files    │      │ uploads/    │
        │ • Logs     │      │  {user_id}/ │
        │ • Users    │      │   {cat}/    │
        │            │      │    file     │
        └────────────┘      └─────────────┘
```

## Request Flow Diagram

```
User Upload Request
    │
    ▼
┌─────────────────────────┐
│  POST /files/           │
│  (multipart/form-data)  │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Authentication    │
    │  (JWT Token)       │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  FileUploadSerializer
    │  • Validate file   │
    │  • Check size      │
    │  • Check MIME type │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  UploadedFileViewSet
    │  perform_create()  │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  UploadedFile Model
    │  Create instance   │
    │  Store metadata    │
    └────────┬───────────┘
             │
    ┌────────┴──────────────────┐
    │                           │
    ▼                           ▼
┌─────────────┐         ┌──────────────┐
│  Database   │         │  File Storage│
│  Save entry │         │  Save file   │
└─────────────┘         └──────────────┘
    │                           │
    │      Response (201)       │
    └───────────────┬───────────┘
                    │
                    ▼
            ┌───────────────┐
            │  JSON Response│
            │  • File ID    │
            │  • File URL   │
            │  • Metadata   │
            └───────────────┘
                    │
                    ▼
              Frontend App
```

## File Storage Structure

```
Backend/
└── media/
    └── uploads/
        └── {user_id}/          # Organized by user
            ├── document/       # PDF, DOC, etc.
            │   ├── report.pdf
            │   ├── notes.docx
            │   └── data.xlsx
            ├── image/          # JPG, PNG, etc.
            │   ├── avatar.jpg
            │   └── screenshot.png
            ├── video/          # MP4, MOV, etc.
            │   └── tutorial.mp4
            ├── audio/          # MP3, WAV, etc.
            │   └── podcast.mp3
            ├── archive/        # ZIP, RAR, etc.
            │   └── backup.zip
            └── other/          # Other files
                └── misc.bin
```

## Database Schema

```
┌────────────────────────────────────────┐
│        file_manager_uploadedfile        │
├────────────────────────────────────────┤
│ id (PK)                    : BigAutoField│
│ created_at                 : DateTime    │
│ updated_at                 : DateTime    │
│ file                       : FileField   │
│ title                      : CharField   │
│ description                : TextField   │
│ category                   : CharField   │
│ file_size                  : BigInteger  │
│ file_type (MIME)          : CharField   │
│ uploaded_by_id (FK)        : BigInteger  │
│ is_public                  : Boolean     │
│ download_count             : Integer     │
│                                          │
│ Indexes:                                 │
│ - (uploaded_by, -created_at)            │
│ - (category, is_public)                 │
└────────────────────────────────────────┘
                  ▲
                  │ 1:N
                  │
┌────────────────────────────────────────┐
│     file_manager_fileaccesslog          │
├────────────────────────────────────────┤
│ id (PK)                    : BigAutoField│
│ created_at                 : DateTime    │
│ updated_at                 : DateTime    │
│ file_id (FK)               : BigInteger  │
│ accessed_by_id (FK, NULL)  : BigInteger  │
│ action                     : CharField   │
│ ip_address                 : GenericIPField│
│                                          │
│ Indexes:                                 │
│ - (file, -created_at)                   │
│ - (accessed_by, -created_at)            │
└────────────────────────────────────────┘
                  △
                  │ N:1
                  │
         ┌────────────────┐
         │ authentication │
         │ User Model     │
         └────────────────┘
```

## Class Relationships

```
┌──────────────────────────────────────────────────────┐
│  UploadedFileViewSet (ViewSet)                       │
├──────────────────────────────────────────────────────┤
│ • queryset: UploadedFile                            │
│ • serializer_class: UploadedFileSerializer          │
│ • permission_classes: [IsAuthenticated,            │
│                        IsFileOwnerOrReadOnly]        │
├──────────────────────────────────────────────────────┤
│ Actions:                                             │
│ + list() - GET /files/                              │
│ + create() - POST /files/                           │
│ + retrieve() - GET /files/{id}/                     │
│ + update() - PUT /files/{id}/                       │
│ + partial_update() - PATCH /files/{id}/             │
│ + destroy() - DELETE /files/{id}/                   │
│ + download() - GET /files/{id}/download/            │
│ + access_logs() - GET /files/{id}/access_logs/      │
│ + my_files() - GET /files/my_files/                 │
│ + public_files() - GET /files/public_files/         │
└──────────────────────────────────────────────────────┘
        │                          │
        │                          │
        ▼                          ▼
  ┌──────────────────────┐  ┌──────────────────────┐
  │ UploadedFile Model   │  │ Serializers          │
  │ • file               │  │ • UploadedFileSer... │
  │ • title              │  │ • FileUploadSer...   │
  │ • category           │  │ • FileAccessLogSer.. │
  │ • uploaded_by        │  └──────────────────────┘
  │ • is_public          │
  │ • download_count     │
  └──────────────────────┘
        │
        └──────────────────────────────────────┐
                                                │
        ┌───────────────────────────────────────┘
        │
        ▼
  ┌──────────────────────┐
  │ FileAccessLog Model  │
  │ • file               │
  │ • accessed_by        │
  │ • action             │
  │ • ip_address         │
  └──────────────────────┘
```

## Permission Flow

```
Request comes in
    │
    ▼
┌─────────────────┐
│ IsAuthenticated │────NO─────▶ HTTP 401
└────────┬────────┘
         │ YES
         ▼
┌──────────────────────┐
│ Determine Action     │
└────────┬─────────────┘
         │
    ┌────┴────┬────────┬────────┬────────┐
    │         │        │        │        │
    ▼         ▼        ▼        ▼        ▼
  LIST    CREATE    RETRIEVE  UPDATE  DELETE
    │         │        │        │        │
    ▼         ▼        ▼        ▼        ▼
  YES    OWNER OK    Public?   OWNER    OWNER
              │       │         │        │
              ▼       ├─YES─┐   ├─YES─┐  ├─YES─┐
             YES      │     │   │     │  │     │
                      NO    │   │     │  │     │
                      │     ▼   ▼     ▼  ▼     ▼
                      └──NO──▶ HTTP 403 (Forbidden)
                              │
                              ▼
                        HTTP 200/201/204
```

## Error Handling Flow

```
Request received
    │
    ▼
Validate input
    │
    ├─ Valid ───▶ Process
    │
    └─ Invalid ──▶ Check error type
                   │
            ┌──────┼──────────┬────────────┐
            │      │          │            │
            ▼      ▼          ▼            ▼
       File size  MIME type  Auth       Permission
       exceeded   invalid    failed      denied
            │      │          │            │
            ▼      ▼          ▼            ▼
       400 Bad   400 Bad   401 Unauth   403 Forbidden
       Request   Request
```

## Data Flow for File Download

```
GET /files/{id}/download/
         │
         ▼
   Authenticate
         │
         ▼
   Check permissions
   (public OR owner)
         │
    ┌────┴──────┐
    │           │
    ▼           ▼
 Allow      Deny
    │           │
    ▼           ▼
 Create    Response
 Log       403 Forbidden
    │
    ▼
 Increment
 download count
    │
    ▼
 Response 200
 with file URL
```

## Integration Points

```
┌─────────────────────────────────────────┐
│          External Systems                │
├─────────────────────────────────────────┤
│                                         │
│  • Authentication System                │
│    └─ JWT Token validation             │
│                                         │
│  • User Model                           │
│    └─ UserProfile, permissions         │
│                                         │
│  • Database (MySQL)                    │
│    └─ File metadata, access logs      │
│                                         │
│  • File Storage System                 │
│    └─ /media directory, volumes       │
│                                         │
│  • Django Admin                        │
│    └─ File management interface       │
│                                         │
│  • REST Framework                      │
│    └─ Serialization, validation       │
│                                         │
└─────────────────────────────────────────┘
```

## Technology Stack

```
┌────────────────────────────┐
│    Technology Stack         │
├────────────────────────────┤
│ Backend Framework          │
│ └─ Django 3.x+             │
│                             │
│ REST API                   │
│ └─ Django REST Framework   │
│                             │
│ Authentication             │
│ └─ JWT (djangorestframework│
│    -simplejwt)             │
│                             │
│ Database                   │
│ └─ MySQL 8.0               │
│                             │
│ File Storage               │
│ └─ Django FileField        │
│    FileSystemStorage       │
│                             │
│ Validation                 │
│ └─ Django validators       │
│    Custom validators       │
│                             │
│ Filtering                  │
│ └─ django-filter           │
│                             │
│ Admin Interface            │
│ └─ Django Admin            │
│                             │
│ Containerization           │
│ └─ Docker                  │
│    Docker Compose          │
└────────────────────────────┘
```
