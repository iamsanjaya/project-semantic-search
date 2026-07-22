"""
Retriever validation tests.

Run:

    python -m tests.test_retriever
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
        file_name="retriever_test_doc.txt",
        page_number=1,
        text=(
            "Python is a high-level programming language. "
            "It is widely used for backend development, "
            "artificial intelligence, and data science. "
            "It supports dynamic typing and garbage collection."
        ),
        metadata={},
    ),
    Page(
        file_name="retriever_test_doc.txt",
        page_number=2,
        text=(
            "PostgreSQL is a relational database system. "
            "It supports ACID transactions and complex queries. "
            "It is commonly used in production systems."
        ),
        metadata={},
    ),
]


def reset_database() -> None:
    """Reset database tables for deterministic testing."""

    with engine.begin() as connection:
        connection.execute(text("DELETE FROM chunks"))
        connection.execute(text("DELETE FROM documents"))

    logger.info("✓ Database reset completed")


def ingest_test_data() -> int:
    """Ingest sample document."""

    pipeline = IngestionPipeline()

    try:
        document_id = pipeline.ingest_document(
            pages=TEST_PAGES,
            source_name="retriever_test_doc.txt",
            source_type="text",
        )

        if not isinstance(document_id, int) or document_id <= 0:
            raise RuntimeError("Invalid document ID returned.")

        logger.info("✓ Test data ingested")

        return document_id

    finally:
        pipeline.close()


def assert_result_schema(result: dict) -> None:
    """Validate retrieval schema."""

    required = {
        "document_id",
        "page_number",
        "chunk_index",
        "text",
        "score",
    }

    missing = required - result.keys()

    if missing:
        raise RuntimeError(f"Missing retrieval fields: {sorted(missing)}")


def test_database_state(document_id: int) -> None:
    """Verify persisted data."""

    with SessionLocal() as session:
        document = session.get(Document, document_id)

        if document is None:
            raise RuntimeError("Document missing.")

        chunks = session.query(Chunk).filter(Chunk.document_id == document_id).all()

        if not chunks:
            raise RuntimeError("No chunks stored.")

    logger.info("✓ Database state verified")


def test_retrieval_basic() -> None:
    """Verify basic retrieval."""

    retriever = Retriever()

    results = retriever.retrieve(
        query="What is Python used for?",
        top_k=3,
    )

    if not results:
        raise RuntimeError("Retriever returned no results.")

    logger.info("✓ Basic retrieval passed")


def test_retrieval_relevance() -> None:
    """Verify semantic relevance."""

    retriever = Retriever()

    results = retriever.retrieve(
        query="What is PostgreSQL?",
        top_k=3,
    )

    if not results:
        raise RuntimeError("Retriever returned no results.")

    first = results[0]

    if "postgresql" not in first["text"].lower():
        raise RuntimeError("Unexpected top retrieval result.")

    logger.info("✓ Retrieval relevance passed")


def test_metadata_and_ranking() -> None:
    """Verify schema and score ordering."""

    retriever = Retriever()

    results = retriever.retrieve(
        query="database transactions ACID",
        top_k=3,
    )

    if len(results) < 2:
        raise RuntimeError("Insufficient retrieval results.")

    for result in results:
        assert_result_schema(result)

    scores = [result["score"] for result in results]

    if scores != sorted(scores, reverse=True):
        raise RuntimeError("Results are not sorted by similarity.")

    logger.info("✓ Ranking validation passed")


def main() -> None:
    """Run the retriever validation suite."""

    logger.info("Running retriever tests...")

    try:
        reset_database()

        document_id = ingest_test_data()

        test_database_state(document_id)
        test_retrieval_basic()
        test_retrieval_relevance()
        test_metadata_and_ranking()

    except Exception:
        logger.exception("Retriever tests failed.")
        sys.exit(1)

    logger.info("All retriever tests passed.")


if __name__ == "__main__":
    main()
