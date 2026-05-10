from django.conf import settings
from django.db import models

from common.constants.enums import VolunteerStatus
from common.db.models import BaseModel


class VolunteerProject(BaseModel):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_projects")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, choices=VolunteerStatus.CHOICES, default=VolunteerStatus.UPCOMING, db_index=True)


class VolunteerEnrollment(BaseModel):
    project = models.ForeignKey(VolunteerProject, on_delete=models.CASCADE, related_name="enrollments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_enrollments")
    hours_contributed = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["project", "user"], name="unique_volunteer_enrollment")]
