# src/domain/page.py

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Page:
    file_name: str
    page_number: int
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
