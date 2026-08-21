from io import BytesIO

import pypdfium2 as pdfium


class PDFRendererService:
    """
    Renders PDF pages into image bytes.

    This service is responsible only for PDF rendering.
    OCR is handled separately by OCRService.
    """

    async def render_pages(
        self,
        content: bytes,
    ) -> list[bytes]:

        if not content:
            raise ValueError(
                "PDF content is required"
            )

        try:
            pdf = pdfium.PdfDocument(content)

            rendered_pages = []

            for page_index in range(len(pdf)):

                page = pdf[page_index]

                bitmap = page.render(
                    scale=2.0
                )

                image = bitmap.to_pil()

                output = BytesIO()

                image.save(
                    output,
                    format="PNG",
                )

                rendered_pages.append(
                    output.getvalue()
                )

                page.close()

            pdf.close()

            return rendered_pages

        except Exception as exc:
            raise ValueError(
                "Invalid PDF content"
            ) from exc