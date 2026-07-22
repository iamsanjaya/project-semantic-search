"""
Document store + ingestion validation tests.

Run:

    python -m tests.test_document_store
"""

from __future__ import annotations

import sys

from sqlalchemy import text

from src.database.database import SessionLocal, engine
from src.database.models import Chunk, Document
from src.domain.page import Page
from src.ingestion.ingest_pipeline import IngestionPipeline
from src.retrieval.retriever import Retriever
from src.utils.logger import logger

TEST_PAGES = [
    Page(
        file_name="test_document.txt",
        page_number=1,
        text=(
            "Python is a high-level programming language. "
            "It supports object-oriented programming and dynamic typing. "
            "It is widely used in artificial intelligence, "
            "web development, and data science."
        ),
        metadata={},
    )
]


def reset_database() -> None:
    """Reset database tables for deterministic testing."""

    with engine.begin() as connection:
        connection.execute(text("DELETE FROM chunks"))
        connection.execute(text("DELETE FROM documents"))

    logger.info("✓ Database reset completed")


def test_ingestion_pipeline() -> int:
    """Verify ingestion pipeline."""

    pipeline = IngestionPipeline()

    document_id = pipeline.ingest_document(
        pages=TEST_PAGES,
        source_name="test_document.txt",
        source_type="text",
    )

    if not isinstance(document_id, int) or document_id <= 0:
        raise RuntimeError("Invalid document ID returned.")

    logger.info("✓ Ingestion pipeline passed")

    return document_id


def test_database_persistence(document_id: int) -> None:
    """Verify persisted document and chunks."""

    with SessionLocal() as session:
        document = session.get(Document, document_id)

        if document is None:
            raise RuntimeError("Document not found.")

        chunks = (
            session.query(Chunk)
            .filter(Chunk.document_id == document_id)
            .order_by(Chunk.chunk_index)
            .all()
        )

        if not chunks:
            raise RuntimeError("No chunks stored.")

        if any(not chunk.chunk_text.strip() for chunk in chunks):
            raise RuntimeError("Empty chunk detected.")

    logger.info("✓ Database persistence passed")


def test_retrieval() -> None:
    """Verify semantic retrieval."""

    retriever = Retriever()

    results = retriever.retrieve(
        query="What is Python?",
        top_k=3,
    )

    if not results:
        raise RuntimeError("Retriever returned no results.")

    first = results[0]

    required_keys = {
        "text",
        "score",
        "document_id",
        "page_number",
        "chunk_index",
    }

    missing = required_keys - first.keys()

    if missing:
        raise RuntimeError(f"Missing retrieval fields: {sorted(missing)}")

    if "python" not in first["text"].lower():
        raise RuntimeError("Unexpected retrieval result.")

    if first["score"] <= 0:
        raise RuntimeError("Similarity score must be positive.")

    logger.info("✓ Retrieval passed")


def main() -> None:
    """Execute the full document-store validation suite."""

    logger.info("Running document store tests...")

    try:
        reset_database()

        document_id = test_ingestion_pipeline()
        test_database_persistence(document_id)
        test_retrieval()

    except Exception:
        logger.exception("Document store tests failed.")
        sys.exit(1)

    logger.info("All document store tests passed.")


if __name__ == "__main__":
    main()
