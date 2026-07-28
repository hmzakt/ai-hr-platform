from __future__ import annotations

import time

import pytesseract
from PIL import Image

from app.parsing.vision.base import BaseVisionProvider
from app.parsing.vision.models import OCRPage, OCRResult


class TesseractVisionProvider(BaseVisionProvider):

    def extract_images(
        self,
        images: list[Image.Image],
    ) -> OCRResult:

        start = time.perf_counter()

        pages: list[OCRPage] = []

        config = "--oem 3 --psm 6"

        for index, image in enumerate(images):

            text = pytesseract.image_to_string(
                image,
                lang="eng",
                config=config,
            )

            pages.append(
                OCRPage(
                    page_number=index + 1,
                    text=text,
                )
            )

        elapsed = int(
            (time.perf_counter() - start) * 1000
        )

        return OCRResult(
            provider="tesseract",
            duration_ms=elapsed,
            pages=pages,
        )
        
        