from __future__ import annotations

import re
from pathlib import Path
from typing import List

import requests
from lxml import html

from src.domain.page import Page
from src.ingestion.base_ingestor import BaseIngestor


class HTMLIngestor(BaseIngestor):
    """
    Production-safe HTML ingestor.

    Supports:
    - Local HTML files (.html/.htm)
    - Remote HTML pages (http/https)

    Extracts semantic content from headings, paragraphs and lists while
    removing common boilerplate elements.
    """

    def _load(self, file_path: str) -> List[Page]:
        # -----------------------------------------
        # Load HTML
        # -----------------------------------------
        if file_path.startswith(("http://", "https://")):
            file_name = file_path.split("/")[-1] or "web_page"

            response = requests.get(
                file_path,
                timeout=10,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0.0.0 Safari/537.36"
                    )
                },
            )

            response.raise_for_status()
            content = response.content

            metadata = {
                "source": "html",
                "url": file_path,
            }

        else:
            path = Path(file_path)

            if not path.exists():
                raise FileNotFoundError(f"HTML file not found: {path}")

            file_name = path.name
            content = path.read_bytes()

            metadata = {
                "source": "html",
                "file_path": str(path),
            }

        tree = html.fromstring(content)

        # -----------------------------------------
        # Remove non-content elements
        # -----------------------------------------
        for node in tree.xpath(
            "//script | //style | //noscript | //header | //footer | //nav | //aside"
        ):
            parent = node.getparent()
            if parent is not None:
                parent.remove(node)

        # -----------------------------------------
        # Extract semantic blocks
        # -----------------------------------------
        blocks = tree.xpath("//h1 | //h2 | //h3 | //p | //li")

        text_parts: List[str] = []

        for block in blocks:
            text = self._normalize(block.text_content())

            if text:
                text_parts.append(text)

        full_text = " ".join(text_parts).strip()

        if not self._is_valid_text(full_text):
            return []

        return [
            Page(
                file_name=file_name,
                page_number=1,
                text=full_text,
                metadata={
                    **metadata,
                    "char_count": len(full_text),
                },
            )
        ]

    # -----------------------------------------
    # Helpers
    # -----------------------------------------

    def _normalize(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\x00", "")
        return text.strip()

    def _is_valid_text(self, text: str) -> bool:
        if not text:
            return False

        if len(text) < 80:
            return False

        alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)

        if alpha_ratio < 0.4:
            return False

        return True
