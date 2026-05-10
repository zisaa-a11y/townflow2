from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.events_calendar.models import Event, EventRsvp
from apps.events_calendar.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["category"]
    search_fields = ["title", "description", "venue"]
    ordering_fields = ["starts_at", "created_at"]

    def get_queryset(self):
        return Event.objects.select_related("creator").prefetch_related("rsvps")

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["post"], url_path="rsvp")
    def rsvp(self, request, pk=None):
        event = self.get_object()
        EventRsvp.objects.get_or_create(event=event, user=request.user)
        return Response(self.get_serializer(event).data)

    @action(detail=True, methods=["post"], url_path="un-rsvp")
    def un_rsvp(self, request, pk=None):
        event = self.get_object()
        EventRsvp.objects.filter(event=event, user=request.user).delete()
        return Response(self.get_serializer(event).data)

    @action(detail=False, methods=["get"], url_path="my-events")
    def my_events(self, request):
        queryset = self.get_queryset().filter(rsvps__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
