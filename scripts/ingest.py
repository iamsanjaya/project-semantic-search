import argparse
import sys
from pathlib import Path

from src.ingestion.ingest_pipeline import IngestionPipeline
from src.ingestion.pdf_ingestor import PDFIngestor
from src.ingestion.docx_ingestor import DOCXIngestor
from src.ingestion.csv_ingestor import CSVIngestor
from src.ingestion.html_ingestor import HTMLIngestor
from src.utils.logger import logger

SUPPORTED_EXTENSIONS = {
    ".pdf": (PDFIngestor, "pdf"),
    ".docx": (DOCXIngestor, "docx"),
    ".csv": (CSVIngestor, "csv"),
}


def ingest_file(pipeline: IngestionPipeline, file_path: Path) -> bool:
    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        logger.warning("Skipping unsupported file: %s", file_path.name)
        return False

    ingestor_cls, source_type = SUPPORTED_EXTENSIONS[extension]

    try:
        ingestor = ingestor_cls()

        logger.info("Processing %s", file_path.name)

        # FIX: use ingest() instead of load()
        pages = ingestor.ingest(str(file_path))

        document_id = pipeline.ingest_document(
            pages=pages,
            source_name=file_path.name,
            source_type=source_type,
        )

        logger.info("Indexed '%s' (Document ID=%d)", file_path.name, document_id)

        return True

    except Exception:
        logger.exception("Failed to ingest '%s'", file_path.name)
        return False


def ingest_directory(
    pipeline: IngestionPipeline, directory: Path, recursive: bool
) -> tuple[int, int]:
    pattern = "**/*" if recursive else "*"

    processed = 0
    failed = 0

    for file_path in sorted(directory.glob(pattern)):
        if not file_path.is_file():
            continue

        if ingest_file(pipeline, file_path):
            processed += 1
        else:
            failed += 1

    return processed, failed


def ingest_url(pipeline: IngestionPipeline, url: str) -> bool:
    try:
        logger.info("Processing %s", url)

        ingestor = HTMLIngestor()

        # FIX: correct variable (url instead of file_path)
        pages = ingestor.ingest(url)

        document_id = pipeline.ingest_document(
            pages=pages,
            source_name=url,
            source_type="web",
        )

        logger.info("Indexed '%s' (Document ID=%d)", url, document_id)

        return True

    except Exception:
        logger.exception("Failed to ingest '%s'", url)
        return False


def parse_args():
    parser = argparse.ArgumentParser(description="Semantic Search Document Ingestion")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--input", help="File or directory to ingest")
    group.add_argument("--url", help="Website URL to ingest")

    parser.add_argument(
        "--recursive", action="store_true", help="Recursively scan directories"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    pipeline = IngestionPipeline()

    try:
        if args.url:
            success = ingest_url(pipeline, args.url)
            sys.exit(0 if success else 1)

        input_path = Path(args.input)

        if not input_path.exists():
            raise FileNotFoundError(f"{input_path} does not exist.")

        if input_path.is_file():
            success = ingest_file(pipeline, input_path)
            sys.exit(0 if success else 1)

        if input_path.is_dir():
            processed, failed = ingest_directory(pipeline, input_path, args.recursive)

            logger.info("Ingestion complete. Processed=%d Failed=%d", processed, failed)

            sys.exit(0 if failed == 0 else 1)

        raise ValueError("Input must be a file or directory.")

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
