from __future__ import annotations

import re
import unicodedata

# Remove ASCII control characters except common whitespace.
_CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

# Collapse consecutive whitespace into a single space.
_WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(text: str | None) -> str:
    """
    Normalize and sanitize extracted text.

    Operations:
    - Handle None safely
    - Unicode normalization (NFKC)
    - Remove NULL bytes
    - Remove control characters
    - Collapse repeated whitespace
    - Trim leading/trailing whitespace
    """
    if not text:
        return ""

    cleaned = unicodedata.normalize("NFKC", text)
    cleaned = cleaned.replace("\x00", "")
    cleaned = _CONTROL_CHAR_PATTERN.sub("", cleaned)
    cleaned = _WHITESPACE_PATTERN.sub(" ", cleaned)

    return cleaned.strip()
