from __future__ import annotations

from pathlib import Path

from src.domain.page import Page
from src.ingestion.ingestor_factory import IngestorFactory
from src.utils.logger import logger


class DocumentLoader:
    """
    Loads supported documents using the appropriate document ingestor.

    Responsibilities
    ----------------
    - Validate the input path.
    - Select the correct ingestor.
    - Convert a document into List[Page].

    This class does NOT:
    - chunk documents
    - generate embeddings
    - persist data
    - perform retrieval
    """

    def __init__(
        self,
        factory: IngestorFactory | None = None,
    ) -> None:
        self._factory = factory or IngestorFactory()

    def load(self, file_path: str | Path) -> list[Page]:
        """
        Load a single document.

        Args:
            file_path:
                Path to a supported document.

        Returns:
            List[Page]

        Raises:
            FileNotFoundError
            ValueError
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise ValueError(f"Not a file: {path}")

        ingestor = self._factory.get_ingestor(path)

        logger.info(
            "Using %s for '%s'",
            ingestor.__class__.__name__,
            path.name,
        )

        pages = ingestor.ingest(str(path))

        logger.info(
            "Loaded %d page(s) from '%s'",
            len(pages),
            path.name,
        )

        return pages

    def supported_extensions(self) -> tuple[str, ...]:
        """
        Return supported file extensions.
        """

        return self._factory.supported_extensions()
