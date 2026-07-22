from typing import Sequence, List
import re

from src.config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from src.domain.chunk import Chunk
from src.domain.page import Page


class TextChunker:
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def _split_sentences(self, text: str) -> list[str]:
        return re.split(r"(?<=[.!?])\s+", text)

    def chunk(self, pages: Sequence[Page]) -> List[Chunk]:
        chunks: List[Chunk] = []
        global_index = 0

        for page in pages:
            text = page.text.strip()
            if not text:
                continue

            sentences = self._split_sentences(text)

            buffer = ""
            for sentence in sentences:
                if len(buffer) + len(sentence) <= self.chunk_size:
                    buffer += " " + sentence
                else:
                    if buffer.strip():
                        chunks.append(
                            Chunk(
                                page_number=page.page_number,
                                chunk_index=global_index,
                                text=buffer.strip(),
                            )
                        )
                        global_index += 1

                    buffer = sentence

            if buffer.strip():
                chunks.append(
                    Chunk(
                        page_number=page.page_number,
                        chunk_index=global_index,
                        text=buffer.strip(),
                    )
                )
                global_index += 1

        return chunks
