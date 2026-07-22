from __future__ import annotations
from typing import Any
from src.embeddings import EmbeddingModel
from src.vectorstore import FAISSStore
from src.utils.logger import logger


class Retriever:
    def __init__(
        self,
        vector_store: FAISSStore | None = None,
        min_score: float = 0.2,
    ) -> None:
        self.vector_store = vector_store or FAISSStore()
        self.min_score = min_score

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filter_by: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        if not query or not query.strip():
            return []

        # 1. embed query
        query_embedding = EmbeddingModel.encode([query])

        # 2. safety check (dimension mismatch detection)
        if hasattr(self.vector_store, "dimension"):
            if len(query_embedding[0]) != self.vector_store.dimension:
                raise ValueError(
                    f"Embedding dim mismatch: "
                    f"{len(query_embedding[0])} != {self.vector_store.dimension}"
                )

        # 3. search
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filter_by=filter_by,
        )

        if not results:
            return []

        # 4. confidence filter — do NOT silently fall back to unfiltered
        # results when nothing clears the bar. If nothing is confident,
        # say so (empty list), so the caller/LLM layer can respond
        # accordingly instead of grounding an answer in noise.
        cleaned = [r for r in results if r.get("score", 0) > self.min_score]

        if not cleaned:
            top_score = results[0].get("score", 0) if results else 0
            logger.warning(
                "No results above min_score=%.2f for query=%r (top raw score=%.4f). "
                "Returning empty — caller should treat as 'insufficient context'.",
                self.min_score,
                query,
                top_score,
            )
            return []

        return cleaned
