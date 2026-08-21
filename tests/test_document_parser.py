import pytest
from unittest.mock import AsyncMock
from app.services.document_parser import DocumentParser


@pytest.mark.asyncio
async def test_parser_returns_supplied_text():

    parser = DocumentParser()

    result = await parser.extract_text(
        filename="claim.txt",
        content="My car was damaged.",
    )

    assert result == "My car was damaged."


@pytest.mark.asyncio
async def test_parser_handles_empty_text_file():

    parser = DocumentParser()

    result = await parser.extract_text(
        filename="claim.txt"
    )

    assert result == ""


@pytest.mark.asyncio
async def test_parser_rejects_unsupported_format():

    parser = DocumentParser()

    with pytest.raises(ValueError):
        await parser.extract_text(
            filename="claim.docx"
        )


@pytest.mark.asyncio
async def test_parser_requires_bytes_for_pdf():

    parser = DocumentParser()

    with pytest.raises(ValueError):
        await parser.extract_text(
            filename="police_report.pdf"
        )


@pytest.mark.asyncio
async def test_parser_rejects_string_pdf_content():

    parser = DocumentParser()

    with pytest.raises(TypeError):
        await parser.extract_text(
            filename="police_report.pdf",
            content="not binary pdf data",
        )

@pytest.mark.asyncio
async def test_image_requires_binary_content():

    parser = DocumentParser()

    with pytest.raises(ValueError):
        await parser.extract_text(
            filename="car_photo.jpg"
        )

@pytest.mark.asyncio
async def test_image_requires_binary_content():

    parser = DocumentParser()

    with pytest.raises(ValueError):
        await parser.extract_text(
            filename="car_photo.jpg"
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


@pytest.mark.asyncio
async def test_parser_ocrs_scanned_pdf():

    ocr_service = AsyncMock()
    ocr_service.extract_text.side_effect = [
        "Police report page one",
        "Police report page two",
    ]

    pdf_renderer_service = AsyncMock()

    pdf_renderer_service.render_pages.return_value = [
        b"page-one-image",
        b"page-two-image",
    ]

    parser = DocumentParser(
        ocr_service=ocr_service,
        pdf_renderer_service=pdf_renderer_service,
    )

    # A valid PDF with no extractable text.
    from io import BytesIO
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(
        width=100,
        height=100,
    )

    output = BytesIO()
    writer.write(output)

    result = await parser.extract_text(
        filename="police_report.pdf",
        content=output.getvalue(),
    )

    assert result == (
        "Police report page one\n\n"
        "Police report page two"
    )

    pdf_renderer_service.render_pages.assert_awaited_once_with(
        output.getvalue()
    )

    assert ocr_service.extract_text.await_count == 2

    ocr_service.extract_text.assert_any_await(
        b"page-one-image",
        "police_report.pdf#page-1",
    )

    ocr_service.extract_text.assert_any_await(
        b"page-two-image",
        "police_report.pdf#page-2",
    )