from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from app.services.pdf_renderer_service import PDFRendererService


class DocumentParser:

    SUPPORTED_TEXT_EXTENSIONS = {
        ".txt",
        ".md",
        ".csv",
    }

    def __init__(
        self,
        ocr_service=None,
        pdf_renderer_service=None,
    ):
        self.ocr_service = ocr_service
        self.pdf_renderer_service = (
            pdf_renderer_service
            or PDFRendererService()
        )

    async def extract_text(
        self,
        filename: str,
        content: str | bytes | None = None,
    ) -> str:

        extension = Path(filename).suffix.lower()

        # -----------------------------------------
        # Validate supported format first
        # -----------------------------------------

        supported_extensions = (
            self.SUPPORTED_TEXT_EXTENSIONS
            | {".pdf", ".jpg", ".jpeg", ".png"}
        )

        if extension not in supported_extensions:
            raise ValueError(
                f"Unsupported document format: {extension}"
            )

        # -----------------------------------------
        # PDF
        # -----------------------------------------

        if extension == ".pdf":

            if content is None:
                raise ValueError(
                    "PDF content is required"
                )

            if isinstance(content, str):
                raise TypeError(
                    "PDF content must be bytes"
                )

            reader = PdfReader(
                BytesIO(content)
            )

            pages = []

            for page in reader.pages:
                text = page.extract_text() or ""

                if text.strip():
                    pages.append(
                        text.strip()
                    )

            extracted_text = "\n\n".join(pages)

            # Text-based PDF
            if extracted_text:
                return extracted_text

            # -------------------------------------
            # Scanned / image-only PDF
            # -------------------------------------

            if self.ocr_service is None:
                raise RuntimeError(
                    "OCR service is not configured"
                )

            rendered_pages = (
                await self.pdf_renderer_service.render_pages(
                    content
                )
            )

            ocr_pages = []

            for page_number, page_content in enumerate(
                rendered_pages,
                start=1,
            ):
                text = await self.ocr_service.extract_text(
                    page_content,
                    f"{filename}#page-{page_number}",
                )

                if text and text.strip():
                    ocr_pages.append(
                        text.strip()
                    )

            return "\n\n".join(ocr_pages)

        # -----------------------------------------
        # Plain text
        # -----------------------------------------

        if extension in self.SUPPORTED_TEXT_EXTENSIONS:

            if content is None:
                return ""

            if isinstance(content, bytes):
                return content.decode("utf-8")

            return content

        # -----------------------------------------
        # Images / OCR
        # -----------------------------------------

        if extension in {".jpg", ".jpeg", ".png"}:

            if content is None:
                raise ValueError(
                    "Image content is required"
                )

            if isinstance(content, str):
                raise TypeError(
                    "Image content must be bytes"
                )

            if self.ocr_service is None:
                raise RuntimeError(
                    "OCR service is not configured"
                )

            return await self.ocr_service.extract_text(
                content,
                filename,
            )