# Generated migration for file_manager app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import apps.file_manager.models
import common.storage.backends


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(storage=common.storage.backends.PublicMediaStorage(), upload_to=apps.file_manager.models.file_upload_path)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('document', 'Document'), ('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('archive', 'Archive'), ('other', 'Other')], db_index=True, max_length=20)),
                ('file_size', models.BigIntegerField(help_text='File size in bytes')),
                ('file_type', models.CharField(help_text='MIME type', max_length=100)),
                ('is_public', models.BooleanField(db_index=True, default=False)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FileAccessLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[('view', 'Viewed'), ('download', 'Downloaded'), ('delete', 'Deleted')], max_length=20)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('accessed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_logs', to='file_manager.uploadedfile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='uploadedfile',
            index=models.Index(fields=['uploaded_by', '-created_at'], name='file_manager_upload_user_idx'),
        ),
        migrations.AddIndex(
            model_name='uploadedfile',
            index=models.Index(fields=['category', 'is_public'], name='file_manager_cat_public_idx'),
        ),
        migrations.AddIndex(
            model_name='fileaccesslog',
            index=models.Index(fields=['file', '-created_at'], name='file_manager_file_log_idx'),
        ),
        migrations.AddIndex(
            model_name='fileaccesslog',
            index=models.Index(fields=['accessed_by', '-created_at'], name='file_manager_user_log_idx'),
        ),
    ]
