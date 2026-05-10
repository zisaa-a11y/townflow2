from django.conf import settings
from django.db import models

from common.constants.enums import EventCategory
from common.db.models import BaseModel
from common.validators.files import validate_image_upload


class Event(BaseModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=EventCategory.CHOICES, db_index=True)
    venue = models.CharField(max_length=255)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField(db_index=True)
    image = models.ImageField(upload_to="events/", blank=True, null=True, validators=[validate_image_upload])

    class Meta:
        ordering = ["starts_at"]
        indexes = [models.Index(fields=["category", "starts_at"])]


class EventRsvp(BaseModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_rsvps")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["event", "user"], name="unique_event_rsvp")]
