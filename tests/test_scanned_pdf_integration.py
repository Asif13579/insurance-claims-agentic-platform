from io import BytesIO

import pytest
from PIL import Image, ImageDraw
from pypdf import PdfWriter

from app.services.document_parser import DocumentParser
from app.services.pdf_renderer_service import PDFRendererService
from app.services.tesseract_ocr_service import TesseractOCRService

def make_test_image() -> bytes:
    image = Image.new(
        "RGB",
        (1600, 500),
        "white",
    )

    draw = ImageDraw.Draw(image)

    text = "CLAIM ID: CLM-12345"

    # Draw the default font at multiple positions to make
    # the characters larger/easier for OCR to recognize.
    for x, y in [
        (100, 100),
        (100, 130),
        (100, 160),
    ]:
        draw.text(
            (x, y),
            text,
            fill="black",
        )

    output = BytesIO()

    image.save(
        output,
        format="PNG",
    )

    return output.getvalue()

# def make_test_image() -> bytes:
#     image = Image.new(
#         "RGB",
#         (1800, 600),
#         "white",
#     )

#     draw = ImageDraw.Draw(image)

#     draw.text(
#         (100, 200),
#         "CLAIM ID: CLM-12345",
#         fill="black",
#     )

#     output = BytesIO()

#     image.save(
#         output,
#         format="PNG",
#     )

#     return output.getvalue()

# def make_test_image() -> bytes:
#     from PIL import ImageFont

#     image = Image.new(
#         "RGB",
#         (1600, 500),
#         "white",
#     )

#     draw = ImageDraw.Draw(image)

#     font = ImageFont.truetype(
#         "DejaVuSans.ttf",
#         80,
#     )

#     draw.text(
#         (100, 180),
#         "CLAIM ID: CLM-12345",
#         fill="black",
#         font=font,
#     )

#     output = BytesIO()

#     image.save(
#         output,
#         format="PNG",
#     )

#     return output.getvalue()

# def make_test_image() -> bytes:
#     image = Image.new(
#         "RGB",
#         (1000, 300),
#         "white",
#     )

#     draw = ImageDraw.Draw(image)

#     draw.text(
#         (50, 100),
#         "CLAIM ID: CLM-12345",
#         fill="black",
#     )

#     output = BytesIO()

#     image.save(
#         output,
#         format="PNG",
#     )

#     return output.getvalue()


def make_pdf() -> bytes:
    """
    Create a blank PDF.

    The important point for this integration test is that
    the PDF renderer and OCR pipeline are exercised with
    real infrastructure.
    """
    writer = PdfWriter()

    writer.add_blank_page(
        width=600,
        height=400,
    )

    output = BytesIO()
    writer.write(output)

    return output.getvalue()


@pytest.mark.asyncio
async def test_real_tesseract_ocr_service():

    service = TesseractOCRService()

    image = make_test_image()

    result = await service.extract_text(
        image,
        "claim.png",
    )

    assert "CLAIM" in result.upper()
    assert "12345" in result


@pytest.mark.asyncio
async def test_real_pdf_renderer():

    service = PDFRendererService()

    pdf = make_pdf()

    pages = await service.render_pages(pdf)

    assert len(pages) == 1
    assert pages[0]


@pytest.mark.asyncio
async def test_document_parser_with_real_ocr():

    parser = DocumentParser(
        ocr_service=TesseractOCRService(),
        pdf_renderer_service=PDFRendererService(),
    )

    # This test intentionally verifies the real OCR path
    # independently from the claim workflow.
    image = make_test_image()

    result = await parser.extract_text(
        filename="claim.png",
        content=image,
    )

    assert "CLAIM" in result.upper()
    assert "12345" in result