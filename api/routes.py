"""
API routes for the Retrieval-Augmented Generation (RAG) application.

This module defines all HTTP endpoints exposed by the application.
The routes are intentionally thin—they validate incoming requests,
delegate business logic to the service layer, and return typed
response models.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from api.schemas import (
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from src.domain.page import Page
from src.services.rag_service import RAGService
from src.utils.logger import logger

API_VERSION = "1.0.0"

router = APIRouter(
    prefix="/api/v1",
    tags=["Retrieval-Augmented Generation"],
)


def get_service(request: Request) -> RAGService:
    """
    Return the application-scoped RAG service.
    """
    service = getattr(request.app.state, "rag_service", None)

    if service is None:
        raise RuntimeError("RAG service is not initialized.")

    return service


RAGServiceDependency = Annotated[RAGService, Depends(get_service)]


@router.get(
    "/health",
    summary="Health Check",
    description="Verify that the API is running.",
    status_code=status.HTTP_200_OK,
)
async def health() -> dict[str, str]:
    logger.info("Health check requested.")

    return {
        "status": "ok",
        "service": "Retrieval-Augmented Generation API",
        "version": API_VERSION,
    }


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Answer",
    description="Retrieve relevant document context and generate a grounded answer.",
)
async def query(
    payload: QueryRequest,
    service: RAGServiceDependency,
) -> QueryResponse:
    result = service.query(
        question=payload.question,
        top_k=payload.top_k,
    )

    return QueryResponse.model_validate(result)


@router.post(
    "/ingest",
    response_model=IngestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest Document",
    description="Ingest a document into the knowledge base.",
)
async def ingest(
    payload: IngestRequest,
    service: RAGServiceDependency,
) -> IngestResponse:
    page = Page(
        file_name=payload.source_name,
        page_number=payload.page_number,
        text=payload.text,
        metadata={},
    )

    result = service.ingest(
        pages=[page],
        source_name=payload.source_name,
        source_type=payload.source_type,
    )

    return IngestResponse.model_validate(result)
