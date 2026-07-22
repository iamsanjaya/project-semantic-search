from __future__ import annotations

from pathlib import Path

from src.ingestion.base_ingestor import BaseIngestor
from src.ingestion.csv_ingestor import CSVIngestor
from src.ingestion.docx_ingestor import DOCXIngestor
from src.ingestion.html_ingestor import HTMLIngestor
from src.ingestion.pdf_ingestor import PDFIngestor
from src.ingestion.text_ingestor import TextIngestor


class IngestorFactory:
    """
    Factory responsible for selecting the correct document ingestor
    based on the file extension.

    Supported formats:
        - .pdf
        - .docx
        - .csv
        - .txt
        - .md
        - .html
        - .htm

    This class does NOT perform ingestion.
    It only returns the appropriate BaseIngestor instance.
    """

    def __init__(self) -> None:
        text_ingestor = TextIngestor()
        html_ingestor = HTMLIngestor()

        self._registry: dict[str, BaseIngestor] = {
            ".pdf": PDFIngestor(),
            ".docx": DOCXIngestor(),
            ".csv": CSVIngestor(),
            ".txt": text_ingestor,
            ".md": text_ingestor,
            ".html": html_ingestor,
            ".htm": html_ingestor,
        }

    def get_ingestor(self, file_path: str | Path) -> BaseIngestor:
        """
        Return the appropriate ingestor for a file.

        Args:
            file_path:
                Path to the source document.

        Returns:
            BaseIngestor implementation.

        Raises:
            ValueError:
                If the file extension is unsupported.
        """

        extension = Path(file_path).suffix.lower()

        ingestor = self._registry.get(extension)

        if ingestor is None:
            supported = ", ".join(sorted(self._registry.keys()))

            raise ValueError(
                f"Unsupported file type '{extension}'. " f"Supported types: {supported}"
            )

        return ingestor

    def supported_extensions(self) -> tuple[str, ...]:
        """
        Return supported file extensions.
        """

        return tuple(sorted(self._registry.keys()))
