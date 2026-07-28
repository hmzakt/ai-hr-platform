from __future__ import annotations

import io
from pathlib import Path

import fitz
from PIL import Image

from app.parsing.builders.document_builder import DocumentBuilder
from app.parsing.cleaners import TextCleaner
from app.parsing.loaders.base import BaseLoader
from app.parsing.models import ParsedPage, ParsedDocument
from app.parsing.vision.base import BaseVisionProvider

from typing import cast


class PDFLoader(BaseLoader):
    """
    Production PDF loader.

    Workflow:
        PDF
          ↓
        Extract native text
          ↓
        OCR fallback (page-wise)
          ↓
        Clean text
          ↓
        Build ParsedDocument
    """

    MIN_TEXT_LENGTH = 30

    def __init__(
        self,
        vision: BaseVisionProvider,
    ) -> None:
        self.vision = vision
        self.cleaner = TextCleaner()
        self.builder = DocumentBuilder()

    def load(self, file: Path) -> ParsedDocument:
        """
        Parse a PDF document.
        """

        document = fitz.open(file)

        pages: list[ParsedPage] = []
        raw_parts: list[str] = []

        ocr_used = False

        for page_number in range(document.page_count):

            page = document.load_page(page_number)

            parsed_page, raw_text = self._parse_page(
                page=page,
                page_number=page_number + 1,
            )

            pages.append(parsed_page)
            raw_parts.append(raw_text)

            ocr_used = ocr_used or parsed_page.ocr_used

        document.close()

        raw_text = "\n\n".join(raw_parts)

        cleaned_text = "\n\n".join(
            page.text for page in pages
        )

        return self.builder.build(
            file=file,
            parser_name=self.__class__.__name__,
            pages=pages,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
            ocr_used=ocr_used,
        )

    def _parse_page(
        self,
        *,
        page: fitz.Page,
        page_number: int,
    ) -> tuple[ParsedPage, str]:
        """
        Parse a single PDF page.
        """

        raw_text = self._extract_text(page)

        used_ocr = False

        if self._needs_ocr(raw_text):
            raw_text = self._extract_with_ocr(page)
            used_ocr = True

        cleaned = self.cleaner.clean(raw_text)

        parsed_page = ParsedPage(
            page_number=page_number,
            text=cleaned,
            ocr_used=used_ocr,
            character_count=len(cleaned),
            word_count=len(cleaned.split()),
            image_count=len(page.get_images(full=True)),
        )

        return parsed_page, raw_text

    @staticmethod
    def _extract_text(page: fitz.Page) -> str:
        """
        Extract searchable text from a PDF page.
        """
        return cast(str, page.get_text("text"))

    def _needs_ocr(self, text: str) -> bool:
        """
        Decide whether OCR is required.
        """

        return len(text.strip()) < self.MIN_TEXT_LENGTH

    def _extract_with_ocr(self, page: fitz.Page) -> str:
        """
        Perform OCR on a single PDF page.
        """

        pixmap = page.get_pixmap(dpi=300)

        image = Image.open(
            io.BytesIO(
                pixmap.tobytes("png")
            )
        )

        result = self.vision.extract_images(
            [image]
        )

        return result.full_text