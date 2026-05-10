from django.urls import path

from apps.ocr_processing.views import OCRProcessAPIView

urlpatterns = [
    path("process/", OCRProcessAPIView.as_view(), name="ocr-process"),
]
