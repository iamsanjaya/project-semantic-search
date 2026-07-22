from src.domain.page import Page
from src.services.rag_service import RAGService


def main() -> None:
    service = RAGService()

    try:
        print("=" * 80)
        print("TESTING INGEST")
        print("=" * 80)

        result = service.ingest(
            pages=[
                Page(
                    file_name="test.txt",
                    page_number=1,
                    text="Python is a high-level programming language.",
                    metadata={},
                )
            ],
            source_name="test.txt",
            source_type="text",
        )

        print(result)
        print()

        print("=" * 80)
        print("TESTING QUERY")
        print("=" * 80)

        result = service.query(
            question="What is Python?",
            top_k=5,
        )

        print(result)

    finally:
        service.close()


if __name__ == "__main__":
    main()
