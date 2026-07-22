from __future__ import annotations

import argparse
import sys

import uvicorn

from src.domain.page import Page
from src.services.rag_service import RAGService
from src.utils.logger import logger


def get_service() -> RAGService:
    return RAGService()


def handle_query(service: RAGService, question: str) -> None:
    result = service.query(question=question)

    print("\nQUESTION")
    print("=" * 72)
    print(result["question"])

    print("\nANSWER")
    print("=" * 72)
    print(result["answer"])

    print("\nSOURCES")
    print("=" * 72)

    sources = result.get("sources", [])

    if not sources:
        print("No sources found.")
        return

    for source in sources:
        score = source.get("score")

        line = (
            f"- document={source.get('document_id')} "
            f"page={source.get('page_number')} "
            f"chunk={source.get('chunk_index')}"
        )

        if score is not None:
            line += f" score={score:.4f}"

        print(line)


def handle_ingest(service: RAGService, text: str) -> None:
    page = Page(
        file_name="cli_input",
        page_number=1,
        text=text,
        metadata={},
    )

    result = service.ingest(
        pages=[page],
        source_name="cli_input",
        source_type="text",
    )

    print("\nINGEST RESULT")
    print("=" * 72)
    print(result)


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Semantic Search CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    query_parser = subparsers.add_parser(
        "query",
        help="Query the knowledge base.",
    )
    query_parser.add_argument(
        "question",
        type=str,
    )

    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Ingest raw text.",
    )
    ingest_parser.add_argument(
        "text",
        type=str,
    )

    args = parser.parse_args()

    service = get_service()

    try:
        if args.command == "query":
            handle_query(service, args.question)

        elif args.command == "ingest":
            handle_ingest(service, args.text)

    finally:
        close = getattr(service, "close", None)
        if callable(close):
            close()


def run_api() -> None:
    uvicorn.run(
        "api.fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py api")
        print("  python main.py query <question>")
        print("  python main.py ingest <text>")
        raise SystemExit(1)

    mode = sys.argv[1]
    sys.argv = [sys.argv[0], *sys.argv[2:]]

    try:
        if mode == "api":
            run_api()
        else:
            run_cli()

    except Exception:
        logger.exception("Application terminated unexpectedly.")
        raise


if __name__ == "__main__":
    main()
