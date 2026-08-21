from io import BytesIO

#from PIL import Image, ImageOps, ImageFilter
from PIL import Image, ImageOps, ImageFilter, UnidentifiedImageError
import pytesseract

from app.services.ocr_service import OCRService


class TesseractOCRService(OCRService):

    async def extract_text(
        self,
        content: bytes,
        filename: str,
    ) -> str:

        if not content:
            raise ValueError(
                "Image content is required"
            )

        if not filename:
            raise ValueError(
                "Filename is required"
            )

        try:
            image = Image.open(
                BytesIO(content)
            )

            image = ImageOps.grayscale(image)
            image = ImageOps.autocontrast(image)

            image = image.resize(
                (
                    image.width * 2,
                    image.height * 2,
                )
            )

            image = image.filter(
                ImageFilter.SHARPEN
            )

        except UnidentifiedImageError as exc:
            raise ValueError(
                "Invalid image content"
            ) from exc

        except Exception as exc:
            raise RuntimeError(
                "Tesseract OCR failed"
            ) from exc

        try:
            text = pytesseract.image_to_string(
                image,
                config="--psm 6",
            )
        except Exception as exc:
            raise RuntimeError(
                "Tesseract OCR failed"
            ) from exc

        return text.strip()