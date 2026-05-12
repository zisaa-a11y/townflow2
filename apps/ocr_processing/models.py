"""Re-export models from models subpackage for backward compatibility."""

from apps.ocr_processing.models.ocr_record import OCRProcessingRecord

__all__ = ["OCRProcessingRecord"]
