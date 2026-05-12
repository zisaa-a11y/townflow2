from django_filters import rest_framework as filters

from apps.file_manager.models import UploadedFile


class UploadedFileFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    is_public = filters.BooleanFilter(field_name="is_public")
    uploaded_by = filters.CharFilter(field_name="uploaded_by__username", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = UploadedFile
        fields = ["category", "is_public", "uploaded_by"]
