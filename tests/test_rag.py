from __future__ import annotations

from src.rag import RAGPipeline
from src.utils.logger import logger


def main() -> None:
    rag = RAGPipeline()

    try:
        response = rag.ask(question="What is Python?")

        print("\nANSWER")
        print("=" * 72)
        print(response["answer"])

        print("\nRETRIEVED SOURCES")
        print("=" * 72)

        sources = response.get("sources", [])

        if not sources:
            print("No sources retrieved.")
            return

        for index, source in enumerate(sources, start=1):
            print(f"\nSource {index}")
            print("-" * 72)

            score = source.get("score")
            if score is not None:
                print(f"Score       : {score:.4f}")

            print(f"Document ID : {source.get('document_id')}")
            print(f"Page Number : {source.get('page_number')}")
            print(f"Chunk Index : {source.get('chunk_index')}")

            text = source.get("text")
            if not text:
                text = source.get("metadata", {}).get("text", "")

            print("\nText")
            print("-" * 72)
            print(text)

    except Exception:
        logger.exception("RAG query failed.")
        raise

    finally:
        close = getattr(rag, "close", None)
        if callable(close):
            close()


if __name__ == "__main__":
    main()
