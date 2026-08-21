from io import BytesIO
from unittest.mock import patch

import pytest
from PIL import Image

from app.services.tesseract_ocr_service import (
    TesseractOCRService,
)


def create_test_image() -> bytes:
    image = Image.new(
        "RGB",
        (100, 50),
        color="white",
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return buffer.getvalue()


@pytest.mark.asyncio
async def test_tesseract_requires_content():

    service = TesseractOCRService()

    with pytest.raises(ValueError):
        await service.extract_text(
            content=b"",
            filename="car_photo.png",
        )


@pytest.mark.asyncio
async def test_tesseract_requires_filename():

    service = TesseractOCRService()

    with pytest.raises(ValueError):
        await service.extract_text(
            content=b"fake-image",
            filename="",
        )


@pytest.mark.asyncio
async def test_tesseract_rejects_invalid_image():

    service = TesseractOCRService()

    with pytest.raises(ValueError):
        await service.extract_text(
            content=b"not-an-image",
            filename="car_photo.png",
        )


@pytest.mark.asyncio
async def test_tesseract_extracts_text():

    service = TesseractOCRService()

    image_content = create_test_image()

    with patch(
        "app.services.tesseract_ocr_service.pytesseract.image_to_string",
        return_value="  Accident vehicle  ",
    ) as mock_ocr:

        result = await service.extract_text(
            content=image_content,
            filename="car_photo.png",
        )

    assert result == "Accident vehicle"

    mock_ocr.assert_called_once()


@pytest.mark.asyncio
async def test_tesseract_passes_image_to_ocr():

    service = TesseractOCRService()

    image_content = create_test_image()

    with patch(
        "app.services.tesseract_ocr_service.pytesseract.image_to_string",
        return_value="Police Report",
    ) as mock_ocr:

        await service.extract_text(
            content=image_content,
            filename="police_report.png",
        )

    image_argument = mock_ocr.call_args.args[0]

    assert isinstance(
        image_argument,
        Image.Image,
    )