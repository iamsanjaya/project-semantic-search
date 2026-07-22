from abc import ABC, abstractmethod
from typing import List
import re
import unicodedata

from src.domain.page import Page


class BaseIngestor(ABC):
    """
    Contract for all document ingestors.
    Ensures only clean + semantically valid text enters pipeline.
    """

    def ingest(self, file_path: str) -> List[Page]:
        raw_pages = self._load(file_path)

        cleaned_pages: List[Page] = []
        for page in raw_pages:
            cleaned = self._clean_page(page)

            if self._is_valid(cleaned.text):
                cleaned_pages.append(cleaned)

        return cleaned_pages

    @abstractmethod
    def _load(self, file_path: str) -> List[Page]:
        pass

    # -----------------------------
    # TEXT CLEANING (syntactic)
    # -----------------------------
    def _clean_page(self, page: Page) -> Page:
        text = page.text or ""

        text = text.replace("\x00", "")
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        return Page(
            file_name=page.file_name,
            page_number=page.page_number,
            text=text,
            metadata=page.metadata or {},
        )

    # -----------------------------
    # SEMANTIC VALIDATION (IMPORTANT)
    # -----------------------------
    def _is_valid(self, text: str) -> bool:
        if not text:
            return False

        text = text.strip()

        # relaxed minimum length (important for QA)
        if len(text) < 20:
            return False

        lowered = text.lower()

        # soft noise detection (NOT hard reject)
        noise_signals = [
            "/type",
            "endobj",
            "stream",
            "/resources",
        ]

        noise_score = sum(sig in lowered for sig in noise_signals)

        # allow small noise, reject only heavily corrupted text
        if noise_score >= 3:
            return False

        # ensure semantic richness
        letters = sum(c.isalpha() for c in text)
        alpha_ratio = letters / max(len(text), 1)

        if alpha_ratio < 0.35:
            return False

        # reject pure metadata-like strings
        if text.count(" ") < 3:
            return False

        return True
