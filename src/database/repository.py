from __future__ import annotations

from typing import Sequence, cast

from src.database.database import SessionLocal
from src.database.models import Chunk as ChunkModel
from src.database.models import Document
from src.domain.chunk import Chunk
from src.utils.logger import logger


class PostgreSQLRepository:
    def __init__(self) -> None:
        self.session = SessionLocal()

    def insert_document(
        self,
        source_name: str,
        source_type: str,
    ) -> int:
        document = Document(
            source_name=source_name,
            source_type=source_type,
        )

        self.session.add(document)
        self.session.flush()
        self.session.refresh(document)

        return cast(int, document.id)

    def insert_chunks(
        self,
        document_id: int,
        chunks: Sequence[Chunk],
    ) -> None:
        if not chunks:
            raise ValueError("No chunks provided for insertion.")

        chunk_models = [
            ChunkModel(
                document_id=document_id,
                chunk_text=chunk.text,
                chunk_index=chunk.chunk_index,
                page_number=chunk.page_number,
            )
            for chunk in chunks
        ]

        self.session.add_all(chunk_models)

        logger.debug(
            "Inserted %d chunks for document %d.",
            len(chunk_models),
            document_id,
        )

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
