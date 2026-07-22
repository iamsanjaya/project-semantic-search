# src/utils/text_normalizer.py

import re
import unicodedata


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)

    text = text.replace("\x00", " ")

    # collapse PDF artifacts
    text = re.sub(r"\s+", " ", text)

    # remove common broken PDF tokens
    text = re.sub(r"obj <<|endobj|stream|endstream", " ", text)

    return text.strip()
