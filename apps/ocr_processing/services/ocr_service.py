import logging

import pytesseract
from django.conf import settings
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError

logger = logging.getLogger(__name__)


class OCRServiceError(Exception):
    pass


class OCRService:
    def __init__(self):
        if settings.OCR_TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.OCR_TESSERACT_CMD

    def preprocess_image(self, image_obj, apply_denoise=None):
        denoise = settings.OCR_APPLY_DENOISE if apply_denoise is None else apply_denoise
        processed = ImageOps.grayscale(image_obj)
        processed = ImageOps.autocontrast(processed)

        if denoise:
            processed = processed.filter(ImageFilter.MedianFilter(size=3))

        return processed

    def cleanup_text(self, text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def extract_text(self, image_file):
        try:
            image = Image.open(image_file)
            processed = self.preprocess_image(image)
            raw_text = pytesseract.image_to_string(
                processed,
                lang=settings.OCR_TESSERACT_LANG,
                config=settings.OCR_TESSERACT_CONFIG,
                timeout=settings.OCR_TIMEOUT_SECONDS,
            )
            return self.cleanup_text(raw_text)
        except (UnidentifiedImageError, OSError) as exc:
            logger.warning("OCR image decode failed", exc_info=exc)
            raise OCRServiceError("Unable to decode the uploaded image for OCR.") from exc
        except RuntimeError as exc:
            logger.warning("OCR timeout reached", exc_info=exc)
            raise OCRServiceError("OCR processing timed out. Please retry with a clearer image.") from exc
        except pytesseract.TesseractError as exc:
            logger.exception("Tesseract OCR failure")
            raise OCRServiceError("OCR engine failed to process the image.") from exc
