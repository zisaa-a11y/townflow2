"""Serializers for OCR Processing module."""

from rest_framework import serializers

from apps.ocr_processing.models import OcrProcessing


class OcrProcessingSerializer(serializers.ModelSerializer):
    """Serializer for OCR processing results."""
    
    user_id = serializers.CharField(source='user.id', read_only=True)
    
    class Meta:
        model = OcrProcessing
        fields = [
            'id',
            'user_id',
            'latitude',
            'longitude',
            'address',
            'extracted_text',
            'metadata',
            'processing_status',
            'error_message',
            'processing_time_ms',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user_id',
            'address',
            'extracted_text',
            'metadata',
            'processing_status',
            'error_message',
            'processing_time_ms',
            'created_at',
            'updated_at',
        ]


class OcrProcessingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating OCR processing requests."""
    
    lat = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6, write_only=True)
    
    class Meta:
        model = OcrProcessing
        fields = ['image', 'lat', 'lon']

    def validate(self, attrs):
        """Validate coordinates."""
        lat = attrs.get('lat')
        lon = attrs.get('lon')
        
        if not (-90 <= float(lat) <= 90):
            raise serializers.ValidationError({'lat': 'Latitude must be between -90 and 90.'})
        if not (-180 <= float(lon) <= 180):
            raise serializers.ValidationError({'lon': 'Longitude must be between -180 and 180.'})
        
        # Map latitude and longitude to the model fields
        attrs['latitude'] = lat
        attrs['longitude'] = lon
        del attrs['lat']
        del attrs['lon']
        return attrs

    def create(self, validated_data):
        """Create OCR processing record with current user."""
        validated_data['user'] = self.context['request'].user
        validated_data['processing_status'] = OcrProcessing.ProcessingStatus.PENDING
        return super().create(validated_data)


class OcrProcessingDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for OCR processing results."""
    
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = OcrProcessing
        fields = [
            'id',
            'user_email',
            'user_name',
            'latitude',
            'longitude',
            'address',
            'extracted_text',
            'metadata',
            'processing_status',
            'error_message',
            'processing_time_ms',
            'created_at',
            'updated_at',
        ]
        read_only_fields = '__all__'


class OcrProcessingListSerializer(serializers.ModelSerializer):
    """Serializer for listing OCR processing results."""
    
    class Meta:
        model = OcrProcessing
        fields = [
            'id',
            'latitude',
            'longitude',
            'address',
            'processing_status',
            'created_at',
        ]
        read_only_fields = '__all__'
