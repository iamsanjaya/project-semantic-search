from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    page_number: int
    chunk_index: int
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
