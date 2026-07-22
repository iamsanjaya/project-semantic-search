"""
Pydantic schemas for the Semantic Search RAG API.

This module defines the request and response models exposed by the HTTP API.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIModel(BaseModel):
    """
    Base model for all API schemas.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )


# ----------------------------------------------------------------------
# Shared Models
# ----------------------------------------------------------------------


class SourceResponse(APIModel):
    """
    Retrieved document chunk returned by the RAG pipeline.
    """

    document_id: int
    source_name: str
    page_number: int
    chunk_index: int
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(APIModel):
    """
    Standard API error response.
    """

    detail: str


# ----------------------------------------------------------------------
# Query
# ----------------------------------------------------------------------


class QueryRequest(APIModel):
    """
    Retrieval-Augmented Generation request.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Natural language question.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Maximum number of results to retrieve.",
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


class QueryResponse(APIModel):
    """
    Retrieval-Augmented Generation response.
    """

    question: str
    answer: str
    sources: list[SourceResponse] = Field(default_factory=list)


# ----------------------------------------------------------------------
# Ingestion
# ----------------------------------------------------------------------


class IngestRequest(APIModel):
    """
    Document ingestion request.
    """

    source_name: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Document filename or identifier.",
    )

    source_type: str = Field(
        default="text",
        min_length=1,
        max_length=50,
        description="Document type (text, pdf, markdown, html, etc.).",
    )

    text: str = Field(
        ...,
        min_length=1,
        description="Raw document text.",
    )

    page_number: int = Field(
        default=1,
        ge=1,
        description="Page number associated with the text.",
    )

    @field_validator("source_name", "source_type", "text")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty.")

        return value


class IngestResponse(APIModel):
    """
    Response returned after successful ingestion.
    """

    document_id: int
    status: str
