"""
Application service layer for the RAG system.

Provides a unified interface for:

- Document ingestion
- Retrieval-Augmented Generation (RAG)
- Response formatting

This service orchestrates the core RAG workflow while remaining independent
from transport layers such as FastAPI or CLI clients.
"""

from __future__ import annotations

from typing import Any, Sequence

from src.generation.llm_service import LLMService
from src.generation.prompt_builder import PromptBuilder
from src.ingestion.ingest_pipeline import IngestionPipeline
from src.domain.page import Page
from src.retrieval.retriever import Retriever
from src.utils.logger import logger


class RAGService:
    """
    High-level application service coordinating the RAG pipeline.

    Responsibilities
    ----------------
    - Validate application inputs.
    - Coordinate document ingestion.
    - Retrieve relevant context.
    - Build grounded prompts.
    - Generate answers using the configured LLM.
    """

    def __init__(
        self,
        ingestion_pipeline: IngestionPipeline | None = None,
        retriever: Retriever | None = None,
        prompt_builder: PromptBuilder | None = None,
        llm_service: LLMService | None = None,
    ) -> None:
        """
        Initialize application services.

        Args:
            ingestion_pipeline:
                Optional ingestion pipeline.

            retriever:
                Optional retriever.

            prompt_builder:
                Optional prompt builder.

            llm_service:
                Optional language model service.
        """

        self.ingestion_pipeline = ingestion_pipeline or IngestionPipeline()

        self.retriever = retriever or Retriever()

        self.prompt_builder = prompt_builder or PromptBuilder()

        self.llm_service = llm_service or LLMService()

    def ingest(
        self,
        pages: Sequence[Page],
        source_name: str,
        source_type: str = "text",
    ) -> dict[str, Any]:
        if not pages:
            raise ValueError("At least one page is required.")

        if not source_name.strip():
            raise ValueError("Source name must not be empty.")

        logger.info(
            "Starting ingestion: source='%s', pages=%d",
            source_name,
            len(pages),
        )

        try:
            document_id = self.ingestion_pipeline.ingest_document(
                pages=pages,
                source_name=source_name,
                source_type=source_type,
            )

            logger.info(
                "Successfully ingested '%s' (document_id=%d).",
                source_name,
                document_id,
            )

            return {
                "document_id": document_id,
                "status": "success",
            }

        except Exception:
            logger.exception(
                "Failed to ingest '%s'.",
                source_name,
            )
        raise

    def query(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Execute a Retrieval-Augmented Generation query.

        Args:
            question:
                User question.

            top_k:
                Number of chunks to retrieve.

        Returns
        -------
        Dictionary containing:

        - question
        - answer
        - sources
        """

        question = question.strip()

        if not question:
            raise ValueError("Question must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        logger.info(
            "Executing RAG query (top_k=%d).",
            top_k,
        )

        try:
            results = self.retriever.retrieve(
                query=question,
                top_k=top_k,
            )

            if not results:
                logger.info("No relevant documents found.")

                return {
                    "question": question,
                    "answer": (
                        "I couldn't find any relevant "
                        "information to answer your question."
                    ),
                    "sources": [],
                }

            logger.info(
                "Retrieved %d chunks.",
                len(results),
            )

            prompt = self.prompt_builder.build_prompt(
                query=question,
                contexts=results,
            )

            generation = self.llm_service.generate(
                prompt=prompt,
            )
            metadata = generation.metadata

            usage = metadata.get("usage", {})

            logger.info(
                (
                    "RAG query completed "
                    "(provider=%s, model=%s, latency_ms=%s, "
                    "total_tokens=%s)"
                ),
                metadata.get("provider"),
                metadata.get("model"),
                metadata.get("latency_ms"),
                usage.get("total_tokens"),
            )

            return {
                "question": question,
                "answer": generation.text,
                "sources": results,
            }

        except Exception:
            logger.exception("RAG query failed.")
            raise

    def close(self) -> None:
        """
        Release resources owned by the service.
        """

        close_method = getattr(
            self.ingestion_pipeline,
            "close",
            None,
        )

        if callable(close_method):
            logger.info("Closing ingestion pipeline.")
            close_method()
