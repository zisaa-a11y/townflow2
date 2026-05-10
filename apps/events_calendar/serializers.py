from rest_framework import serializers

from apps.events_calendar.models import Event, EventRsvp


class EventSerializer(serializers.ModelSerializer):
    attendee_count = serializers.IntegerField(source="rsvps.count", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "creator",
            "title",
            "description",
            "category",
            "venue",
            "starts_at",
            "ends_at",
            "image",
            "attendee_count",
            "created_at",
        ]
        read_only_fields = ["id", "creator", "attendee_count", "created_at"]


class EventRsvpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        fields = ["id", "event", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
