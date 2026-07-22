import argparse
import sys

from src.rag.rag_pipeline import RAGPipeline
from src.utils.logger import logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Semantic Search Query CLI",
    )

    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="Question to ask the RAG system.",
    )

    parser.add_argument(
        "-k",
        "--top-k",
        type=int,
        default=5,
        help="Number of documents to retrieve (default: 5).",
    )

    return parser.parse_args()


def print_response(response: dict) -> None:
    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(response["question"])

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(response["answer"])

    sources = response.get("sources", [])

    print("\n" + "=" * 80)
    print(f"SOURCES ({len(sources)})")
    print("=" * 80)

    if not sources:
        print("No sources found.")
        return

    for index, source in enumerate(sources, start=1):
        print(f"\n[{index}]")
        print(f"Document ID : {source.get('document_id')}")
        print(f"Page        : {source.get('page_number')}")
        print(f"Chunk       : {source.get('chunk_index')}")

        score = source.get("score")
        if score is not None:
            print(f"Score       : {score:.4f}")

        text = source.get("text", "")

        if text:
            preview = text.strip()
            if len(preview) > 300:
                preview = preview[:300] + "..."

            print(f"Preview     : {preview}")


def main():
    args = parse_args()

    pipeline = RAGPipeline()

    try:
        response = pipeline.ask(
            question=args.query,
            top_k=args.top_k,
        )

        print_response(response)

    except Exception:
        logger.exception("Search failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
