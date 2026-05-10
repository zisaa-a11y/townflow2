from decimal import Decimal

from rest_framework import serializers


def validate_latitude(value):
    value = Decimal(value)
    if value < Decimal("-90") or value > Decimal("90"):
        raise serializers.ValidationError("Latitude must be between -90 and 90.")
    return value


def validate_longitude(value):
    value = Decimal(value)
    if value < Decimal("-180") or value > Decimal("180"):
        raise serializers.ValidationError("Longitude must be between -180 and 180.")
    return value
