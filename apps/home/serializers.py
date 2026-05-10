from rest_framework import serializers

from apps.home.models import HomeBanner, QuickAction


class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBanner
        fields = ["id", "title", "subtitle", "cta_label", "cta_route"]


class QuickActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickAction
        fields = ["id", "name", "route_key", "icon_key", "sort_order"]
