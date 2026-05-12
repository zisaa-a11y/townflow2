#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if doesn't exist
if not User.objects.filter(email='admin@townflow.com').exists():
    user = User.objects.create_superuser(
        email='admin@townflow.com',
        full_name='Admin User',
        password='Admin@123'
    )
    print("✅ Superuser created successfully!")
    print(f"📧 Email: {user.email}")
    print(f"🔐 Password: Admin@123")
else:
    print("ℹ️ Superuser already exists")

# List all admin users
admins = User.objects.filter(role='admin')
print(f"\n👥 Total Admin Accounts: {admins.count()}")
for admin in admins:
    print(f"  - {admin.email} ({admin.full_name})")
