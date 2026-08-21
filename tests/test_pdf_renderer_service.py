from io import BytesIO

import pytest
from pypdf import PdfWriter

from app.services.pdf_renderer_service import PDFRendererService


def make_pdf() -> bytes:
    writer = PdfWriter()

    writer.add_blank_page(
        width=100,
        height=100,
    )

    output = BytesIO()
    writer.write(output)

    return output.getvalue()


@pytest.mark.asyncio
async def test_renderer_requires_content():

    service = PDFRendererService()

    with pytest.raises(ValueError):
        await service.render_pages(b"")


@pytest.mark.asyncio
async def test_renderer_rejects_invalid_pdf():

    service = PDFRendererService()

    with pytest.raises(ValueError):
        await service.render_pages(
            b"not-a-real-pdf"
        )


@pytest.mark.asyncio
async def test_renderer_returns_pages_for_valid_pdf():

    service = PDFRendererService()

    result = await service.render_pages(
        make_pdf()
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], bytes)
    assert result[0]