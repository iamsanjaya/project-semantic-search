"""
Basic infrastructure connectivity tests.

Run:

    python -m tests.test_connection
"""

from __future__ import annotations

import sys

from sqlalchemy import text

from src.database.database import engine
from src.embeddings.embedding_model import EmbeddingModel
from src.utils.logger import logger
from src.vectorstore.faiss_store import FAISSStore


def test_database_connection() -> None:
    """Verify PostgreSQL connectivity."""

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        if result.scalar_one() != 1:
            raise RuntimeError("Database connectivity test failed.")

    logger.info("✓ PostgreSQL connection successful")


def test_embedding_model() -> None:
    """Verify the embedding model loads and produces a valid embedding."""

    embedding = EmbeddingModel.encode("Connection test")

    if embedding.size == 0:
        raise RuntimeError("Embedding model returned an empty embedding.")

    logger.info(
        "✓ Embedding model loaded successfully (dimension=%d)",
        embedding.shape[0],
    )


def test_faiss_store() -> None:
    """Verify the FAISS vector store initializes successfully."""

    store = FAISSStore()

    if store.index is None:
        raise RuntimeError("FAISS index failed to initialize.")

    if store.index.ntotal < 0:
        raise RuntimeError("Invalid FAISS index state.")

    logger.info(
        "✓ FAISS store initialized successfully (%d vectors)",
        store.index.ntotal,
    )


def main() -> None:
    """Run all infrastructure connectivity tests."""

    logger.info("Running infrastructure connectivity tests...")

    try:
        test_database_connection()
        test_embedding_model()
        test_faiss_store()

    except Exception:
        logger.exception("Infrastructure connectivity tests failed.")
        sys.exit(1)

    logger.info("All infrastructure connectivity tests passed.")


if __name__ == "__main__":
    main()
