from __future__ import annotations

from src.domain.page import Page
from src.ingestion.ingest_pipeline import IngestionPipeline
from src.utils.logger import logger


def main() -> None:
    pipeline = IngestionPipeline()

    try:
        text = """
        Python is a high-level programming language.

        It supports object-oriented programming.

        Python is widely used in artificial intelligence,
        machine learning, and web development.
        """

        pages = [
            Page(
                file_name="python.txt",
                page_number=1,
                text=text.strip(),
                metadata={},
            )
        ]

        document_id = pipeline.ingest_document(
            pages=pages,
            source_name="python.txt",
            source_type="text",
        )

        logger.info("Document ingested successfully.")
        logger.info("Document ID: %d", document_id)

    except Exception:
        logger.exception("Document ingestion failed.")
        raise

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
