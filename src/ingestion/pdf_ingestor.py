import fitz
from typing import List

from src.ingestion.base_ingestor import BaseIngestor
from src.domain.page import Page


class PDFIngestor(BaseIngestor):
    """
    Production-grade PDF ingestor.
    Guarantees semantic-only text extraction (no PDF object leakage).
    """

    def _load(self, file_path: str) -> List[Page]:
        doc = fitz.open(file_path)

        try:
            pages: List[Page] = []
            file_name = file_path.split("/")[-1]

            for page_number in range(len(doc)):
                page = doc.load_page(page_number)

                # -----------------------------------------
                # STRONG EXTRACTION MODE (BLOCK TEXT FIRST)
                # -----------------------------------------
                blocks = page.get_text("blocks")

                if not blocks:
                    continue

                text_parts = []

                for block in blocks:
                    if len(block) < 5:
                        continue

                    raw = block[4]  # text field

                    if not isinstance(raw, str):
                        continue

                    cleaned = raw.strip()

                    # -----------------------------------------
                    # HARD FILTER: remove PDF artifacts
                    # -----------------------------------------
                    lowered = cleaned.lower()

                    if any(
                        x in lowered
                        for x in [
                            "/type",
                            "/page",
                            "obj <<",
                            "/resources",
                            "/font",
                            "endobj",
                            "stream",
                        ]
                    ):
                        continue

                    if len(cleaned) < 20:
                        continue

                    text_parts.append(cleaned)

                text = " ".join(text_parts).strip()

                # -----------------------------------------
                # FINAL VALIDATION
                # -----------------------------------------
                if not text:
                    continue

                alpha_ratio = sum(c.isalpha() for c in text) / len(text)

                # reject garbage pages
                if alpha_ratio < 0.45:
                    continue

                pages.append(
                    Page(
                        file_name=file_name,
                        page_number=page_number + 1,
                        text=text,
                        metadata={
                            "source": "pdf",
                            "file_path": file_path,
                            "char_count": len(text),
                        },
                    )
                )

            return pages

        finally:
            doc.close()
