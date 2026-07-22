"""
LLM service for Retrieval-Augmented Generation (RAG).

This module provides a provider-neutral interface for text generation while
using Groq as the underlying LLM provider.

Responsibilities
----------------
- Initialize and manage the Groq client.
- Submit prompts to the configured language model.
- Validate LLM responses.
- Return provider-neutral generation results.
- Record generation latency and token usage.

This service intentionally does NOT:
- Retrieve documents.
- Build prompts.
- Perform FastAPI request handling.
- Apply retry policies.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any

from groq import Groq

from src.config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_TIMEOUT,
)
from src.utils.logger import logger


@dataclass(frozen=True)
class GenerationResult:
    """
    Provider-neutral generation result.

    Attributes
    ----------
    text:
        Generated response text.

    metadata:
        Additional provider metadata useful for observability,
        debugging and future extensions.
    """

    text: str
    metadata: dict[str, Any]


class LLMService:
    """
    Service responsible for communicating with the configured LLM.

    The service hides provider-specific implementation details behind
    a simple interface returning a provider-neutral GenerationResult.
    """

    def __init__(self) -> None:
        """
        Initialize the Groq client.
        """

        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not configured.")

        self._client = Groq(
            api_key=GROQ_API_KEY,
            timeout=GROQ_TIMEOUT,
        )

        self._model = GROQ_MODEL
        self._default_temperature = GROQ_TEMPERATURE

    def generate(
        self,
        prompt: str,
        *,
        temperature: float | None = None,
    ) -> GenerationResult:
        """
        Generate an answer from the configured LLM.

        Parameters
        ----------
        prompt:
            Fully constructed prompt.

        temperature:
            Optional sampling temperature. If omitted,
            the configured default is used.

        Returns
        -------
        GenerationResult
            Provider-neutral generation result.

        Raises
        ------
        ValueError
            If the prompt is empty.

        RuntimeError
            If generation fails or the provider returns
            an invalid response.
        """

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        temperature = self._default_temperature if temperature is None else temperature

        if not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0.")

        start = perf_counter()

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

        except Exception as exc:
            logger.exception("LLM generation failed.")
            raise RuntimeError("Failed to generate response from LLM.") from exc

        elapsed_ms = round(
            (perf_counter() - start) * 1000,
            2,
        )

        if not response.choices:
            raise RuntimeError("LLM returned no completion choices.")

        choice = response.choices[0]

        if choice.message is None:
            raise RuntimeError("LLM returned an empty message.")

        text = choice.message.content

        if not text:
            raise RuntimeError("LLM returned empty content.")

        usage = response.usage

        metadata = {
            "provider": "groq",
            "model": response.model,
            "finish_reason": choice.finish_reason,
            "latency_ms": elapsed_ms,
            "usage": {
                "prompt_tokens": (usage.prompt_tokens if usage else 0),
                "completion_tokens": (usage.completion_tokens if usage else 0),
                "total_tokens": (usage.total_tokens if usage else 0),
            },
        }
        logger.info(
            (
                "LLM generation completed "
                "(provider=%s, model=%s, latency_ms=%.2f, "
                "prompt_tokens=%d, completion_tokens=%d, total_tokens=%d)"
            ),
            metadata["provider"],
            metadata["model"],
            metadata["latency_ms"],
            metadata["usage"]["prompt_tokens"],
            metadata["usage"]["completion_tokens"],
            metadata["usage"]["total_tokens"],
        )

        return GenerationResult(
            text=text.strip(),
            metadata=metadata,
        )
