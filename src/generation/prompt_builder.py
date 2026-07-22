"""
Prompt builder for Retrieval-Augmented Generation (RAG).

This module is responsible for transforming a user's query and
retrieved document chunks into a grounded prompt suitable for
Large Language Models.

Responsibilities:
- Format retrieved context consistently.
- Apply grounding instructions.
- Limit prompt size.
- Keep prompt construction independent of retrieval and LLM providers.
"""

from __future__ import annotations

from collections.abc import Sequence
from textwrap import dedent
from typing import Any, Final


class PromptBuilder:
    """
    Builds grounded prompts for Retrieval-Augmented Generation.

    The PromptBuilder has no knowledge of:
        - FAISS
        - PostgreSQL
        - FastAPI
        - Groq/OpenAI/etc.

    It only formats retrieved context into a prompt.
    """

    DEFAULT_MAX_CONTEXT_CHARS: Final[int] = 12_000

    SYSTEM_PROMPT = dedent("""
        You are a helpful AI assistant.

        Answer the user's question using ONLY the supplied context.

        Rules:
        - Do not invent or assume facts.
        - If the answer is not contained in the context, clearly say:
          "I don't have enough information in the provided documents to answer that."
        - Do not reference information outside the supplied context.
        - Prefer concise, accurate answers.
        - If multiple context sections contribute to the answer, combine them naturally.
        """).strip()

    def __init__(
        self,
        max_context_chars: int | None = None,
    ) -> None:
        if max_context_chars is not None and max_context_chars <= 0:
            raise ValueError("max_context_chars must be greater than zero.")

        self.max_context_chars = (
            max_context_chars
            if max_context_chars is not None
            else self.DEFAULT_MAX_CONTEXT_CHARS
        )

    def build_prompt(
        self,
        query: str,
        contexts: Sequence[dict[str, Any]],
    ) -> str:
        """
        Build a complete prompt for the LLM.
        """

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        formatted_context = self._format_context(contexts)

        return dedent(f"""
            {self.SYSTEM_PROMPT}

            =========================
            CONTEXT
            =========================

            {formatted_context}

            =========================
            USER QUESTION
            =========================

            {query}

            =========================
            ANSWER
            =========================
            """).strip()

    def _format_context(
        self,
        contexts: Sequence[dict[str, Any]],
    ) -> str:
        """
        Format retrieved document chunks.

        Context is truncated once the configured maximum
        number of characters has been reached.
        """

        if not contexts:
            return "No relevant context was retrieved."

        sections: list[str] = []
        current_size = 0

        for i, context in enumerate(contexts, start=1):
            raw_text = context.get("text", "")

            if not isinstance(raw_text, str):
                continue

            text = self._clean_text(raw_text)

            if not text:
                continue

            source_name = str(context.get("source_name", "Unknown"))

            page = context.get("page_number")

            header = [
                f"Context {i}",
                f"Source: {source_name}",
            ]

            if page is not None:
                header.append(f"Page: {page}")

            section = "\n".join(header)
            section += "\n" + "-" * 40 + "\n"
            section += text

            if current_size + len(section) > self.max_context_chars:
                break

            sections.append(section)
            current_size += len(section)

        if not sections:
            return "No usable context was retrieved."

        return "\n\n".join(sections)

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Normalize retrieved text before inserting it into the prompt.
        """

        return " ".join(text.split())
