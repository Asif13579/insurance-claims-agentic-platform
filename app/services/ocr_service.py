class OCRService:
    """
    OCR abstraction.

    The service owns OCR infrastructure.
    Agents should depend on this interface rather than
    directly depending on Tesseract or another OCR engine.
    """

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

        raise NotImplementedError(
            "OCR engine will be implemented in Phase 7.3"
        )