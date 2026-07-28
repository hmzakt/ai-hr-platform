from pathlib import Path
import mimetypes

from app.parsing.models import (
    ParsedDocument,
    ParsedPage,
    DocumentMetadata,
)
from app.parsing.utils.hashing import sha256_file


class DocumentBuilder:

    PARSER_VERSION = "1.0"

    def build(
        self,
        *,
        file: Path,
        parser_name: str,
        pages: list[ParsedPage],
        raw_text: str,
        cleaned_text: str,
        encoding: str | None = None,
        language: str | None = None,
        ocr_used: bool = False,
    ) -> ParsedDocument:

        metadata = DocumentMetadata(
            filename=file.name,
            extension=file.suffix,
            mime_type=mimetypes.guess_type(file)[0],
            parser_name=parser_name,
            parser_version=self.PARSER_VERSION,
            file_size_bytes=file.stat().st_size,
            page_count=len(pages),
            encoding=encoding,
            language=language,
            ocr_used=ocr_used,
            sha256=sha256_file(file),
        )

        return ParsedDocument(
            source_path=file,
            extension=file.suffix,
            metadata=metadata,
            pages=pages,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
        )
