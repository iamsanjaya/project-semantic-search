from __future__ import annotations

from pathlib import Path
from typing import List

from src.domain.page import Page
from src.ingestion.base_ingestor import BaseIngestor


class TextIngestor(BaseIngestor):
    """
    Ingest plain text and Markdown documents.

    Supports:
    - .txt
    - .md

    Produces a single Page for the document.
    Cleaning and validation are handled by BaseIngestor.
    """

    def _load(self, file_path: str) -> List[Page]:
        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        if not text:
            return []

        return [
            Page(
                file_name=path.name,
                page_number=1,
                text=text,
                metadata={
                    "source": "text",
                    "file_path": str(path),
                    "char_count": len(text),
                },
            )
        ]
