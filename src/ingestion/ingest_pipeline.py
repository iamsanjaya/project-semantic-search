from src.chunking import TextChunker
from src.database.repository import PostgreSQLRepository
from src.embeddings import EmbeddingModel
from src.vectorstore import FAISSStore
from src.utils.logger import logger
from src.domain.chunk import Chunk
from src.domain.page import Page
from typing import Sequence, List
from src.utils.text_normalizer import normalize_text


class IngestionPipeline:
    def __init__(
        self,
        chunker: TextChunker | None = None,
        repository: PostgreSQLRepository | None = None,
        vector_store: FAISSStore | None = None,
    ):
        self.chunker = chunker or TextChunker()
        self.repository = repository or PostgreSQLRepository()
        self.vector_store = vector_store or FAISSStore()

    # -----------------------------
    # VALIDATION (STRICT CONTRACT)
    # -----------------------------
    def _validate_pages(self, pages: Sequence[Page]) -> None:
        if not pages:
            raise ValueError("Empty document provided")

        for page in pages:
            if not isinstance(page.text, str):
                raise ValueError("Page text must be string")

            text = page.text

            if not text or not text.strip():
                raise ValueError(f"Empty page detected: {page.page_number}")

            if "\x00" in text:
                raise ValueError(f"Null byte detected in page {page.page_number}")

    # -----------------------------
    # SINGLE CANONICAL CLEANING
    # -----------------------------
    def _prepare_pages(self, pages: Sequence[Page]) -> List[Page]:
        cleaned_pages: List[Page] = []

        for p in pages:
            text = normalize_text(p.text)

            if not text:
                continue

            cleaned_pages.append(
                Page(
                    file_name=p.file_name,
                    page_number=p.page_number,
                    text=text,
                    metadata=p.metadata or {},
                )
            )

        return cleaned_pages

    # -----------------------------
    # MAIN PIPELINE
    # -----------------------------
    def ingest_document(
        self,
        pages: Sequence[Page],
        source_name: str,
        source_type: str,
    ) -> int:
        try:
            # 1. validate raw input
            self._validate_pages(pages)

            # 2. canonical cleaning (ONLY CLEANING STAGE)
            clean_pages = self._prepare_pages(pages)

            if not clean_pages:
                raise ValueError("No valid pages after cleaning")

            # 3. chunking (expects already-clean text)
            chunks: List[Chunk] = self.chunker.chunk(clean_pages)

            if not chunks:
                raise ValueError("No chunks generated from document")

            logger.info(
                "Generated %d chunks for '%s'",
                len(chunks),
                source_name,
            )

            # 4. persist document
            document_id = self.repository.insert_document(
                source_name=source_name,
                source_type=source_type,
            )

            self.repository.insert_chunks(
                document_id=document_id,
                chunks=chunks,
            )

            # 5. embeddings
            embeddings = EmbeddingModel.encode([c.text for c in chunks])

            metadata = [
                {
                    "document_id": document_id,
                    "page_number": c.page_number,
                    "chunk_index": c.chunk_index,
                    "source_name": source_name,
                    "source_type": source_type,
                    "text": c.text,
                }
                for c in chunks
            ]

            # 6. vector store (critical consistency boundary)
            try:
                self.vector_store.add(
                    embeddings=embeddings,
                    metadata=metadata,
                )
                self.vector_store.save()

            except Exception as e:
                self.repository.rollback()
                raise RuntimeError(f"Vector store failure, rolled back DB: {e}")

            # 7. commit after successful vector write
            self.repository.commit()

            logger.info(
                "Successfully ingested '%s' (ID=%d)",
                source_name,
                document_id,
            )

            return document_id

        except Exception:
            self.repository.rollback()
            logger.exception("Ingestion failed for '%s'", source_name)
            raise

    def close(self) -> None:
        self.repository.close()
