from django.conf import settings
from django.db import models

from common.constants.enums import BloodRequestStatus, BloodRequestUrgency
from common.db.models import BaseModel


class BloodGroup(BaseModel):
    name = models.CharField(max_length=10, unique=True)


class DonorProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donor_profile")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT, related_name="donors")
    last_donated_at = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


class BloodRequest(BaseModel):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blood_requests")
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.PROTECT, related_name="requests")
    units_needed = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=10, choices=BloodRequestUrgency.CHOICES, default=BloodRequestUrgency.NORMAL)
    status = models.CharField(max_length=20, choices=BloodRequestStatus.CHOICES, default=BloodRequestStatus.PENDING)
    hospital_name = models.CharField(max_length=255)
    required_by = models.DateTimeField(db_index=True)
    notes = models.TextField(blank=True)


class BloodRequestMatch(BaseModel):
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name="matches")
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name="matches")
    accepted = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["blood_request", "donor"], name="unique_blood_match")]
