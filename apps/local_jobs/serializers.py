from rest_framework import serializers

from apps.local_jobs.models import Job, JobApplication


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "posted_by",
            "title",
            "description",
            "company_name",
            "location",
            "job_type",
            "salary_min",
            "salary_max",
            "deadline",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "posted_by", "created_at"]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "job", "applicant", "cover_letter", "resume_url", "created_at"]
        read_only_fields = ["id", "applicant", "created_at"]
