import pytest
from unittest.mock import AsyncMock

from app.services.ocr_service import OCRService
from app.services.document_parser import DocumentParser

@pytest.mark.asyncio
async def test_ocr_requires_content():

    service = OCRService()

    with pytest.raises(ValueError):
        await service.extract_text(
            content=b"",
            filename="car_photo.jpg",
        )


@pytest.mark.asyncio
async def test_ocr_requires_filename():

    service = OCRService()

    with pytest.raises(ValueError):
        await service.extract_text(
            content=b"fake-image",
            filename="",
        )


@pytest.mark.asyncio
async def test_ocr_engine_is_not_implemented_yet():

    service = OCRService()

    with pytest.raises(NotImplementedError):
        await service.extract_text(
            content=b"fake-image",
            filename="car_photo.jpg",
        )

@pytest.mark.asyncio
async def test_parser_delegates_image_to_ocr_service():

    ocr_service = AsyncMock()

    ocr_service.extract_text.return_value = (
        "Accident report text"
    )

    parser = DocumentParser(
        ocr_service=ocr_service
    )

    content = b"fake-image-bytes"

    result = await parser.extract_text(
        filename="accident.jpg",
        content=content,
    )

    assert result == "Accident report text"

    ocr_service.extract_text.assert_awaited_once_with(
        content,
        "accident.jpg",
    )