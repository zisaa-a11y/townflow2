from django.db import models

from common.db.models import BaseModel


class HomeBanner(BaseModel):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    cta_label = models.CharField(max_length=120, blank=True)
    cta_route = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)


class QuickAction(BaseModel):
    name = models.CharField(max_length=100)
    route_key = models.CharField(max_length=80, unique=True)
    icon_key = models.CharField(max_length=80)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["sort_order", "name"]
