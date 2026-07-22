from src.generation import GroqGenerator
from src.rag.context_builder import ContextBuilder
from src.retrieval import Retriever


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.context_builder = ContextBuilder()
        self.generator = GroqGenerator()

    def ask(
        self,
        question: str,
        top_k: int = 5,
        filter_by: dict | None = None,
    ) -> dict:

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        retrieved_chunks = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            filter_by=filter_by,
        )

        context = self.context_builder.build(retrieved_chunks)

        answer = self.generator.generate(
            question=question,
            context=context,
        )

        # Normalize sources into stable API contract
        sources = [
            {
                "score": chunk.get("score"),
                "document_id": chunk.get("document_id"),
                "page_number": chunk.get("page_number"),
                "chunk_index": chunk.get("chunk_index"),
                "text": chunk.get("text") or chunk.get("metadata", {}).get("text"),
                # keep full metadata only as fallback (optional debugging)
                "metadata": chunk.get("metadata", {}),
            }
            for chunk in retrieved_chunks
        ]

        return {
            "question": question,
            "answer": answer,
            "context": context,
            # clean, structured output (this is now your API contract)
            "sources": sources,
        }
