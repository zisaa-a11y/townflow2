from django.conf import settings
from django.db import models

from common.constants.enums import JobType
from common.db.models import BaseModel


class Job(BaseModel):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JobType.CHOICES, db_index=True)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)


class JobApplication(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_applications")
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["job", "applicant"], name="unique_job_application")]
