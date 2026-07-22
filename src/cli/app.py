from __future__ import annotations

from pathlib import Path

from src.ingestion.document_loader import DocumentLoader
from src.services.rag_service import RAGService
from src.utils.logger import logger


class CLIApp:
    VERSION = "semantic-search v0.1.0"

    def __init__(self) -> None:
        self._service: RAGService | None = None

    def _get_service(self) -> RAGService:
        if self._service is None:
            self._service = RAGService()
        return self._service

    def _close(self) -> None:
        if self._service is not None:
            close = getattr(self._service, "close", None)
            if callable(close):
                close()
            self._service = None

    def version(self) -> str:
        return self.VERSION

    def query(self, question: str, top_k: int = 5) -> dict:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be greater than 0.")

        service = self._get_service()

        try:
            result = service.query(
                question=question.strip(),
                top_k=top_k,
            )

            return {
                "question": result["question"],
                "answer": result["answer"],
                "sources": result["sources"],
            }

        finally:
            self._close()

    def ingest(self, source_path: str = "data/raw") -> dict:
        root = Path(source_path)

        if not root.exists():
            raise FileNotFoundError(f"Path not found: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Not a directory: {root}")

        service = self._get_service()
        loader = DocumentLoader()

        supported_extensions = set(loader.supported_extensions())

        total_files = 0
        skipped_files = 0

        try:
            for file in sorted(root.rglob("*")):
                if not file.is_file():
                    continue

                if file.suffix.lower() not in supported_extensions:
                    logger.info(
                        "Skipping unsupported file: %s",
                        file.name,
                    )
                    skipped_files += 1
                    continue

                try:
                    pages = loader.load(file)

                    if not pages:
                        logger.warning(
                            "No valid content extracted from %s",
                            file.name,
                        )
                        skipped_files += 1
                        continue

                    service.ingest(
                        pages=pages,
                        source_name=file.name,
                        source_type=file.suffix.lstrip(".").lower(),
                    )

                    total_files += 1

                except Exception:
                    logger.exception(
                        "Failed to ingest file: %s",
                        file,
                    )
                    skipped_files += 1

            return {
                "status": "success",
                "files_ingested": total_files,
                "files_skipped": skipped_files,
            }

        finally:
            self._close()
