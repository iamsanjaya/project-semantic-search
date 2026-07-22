"""
FastAPI application entry point for the Semantic Search RAG system.

Responsibilities:
    - Create the FastAPI application
    - Configure application metadata
    - Manage application lifecycle
    - Register global exception handlers
    - Register API routers
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.routes import router
from api.schemas import ErrorResponse
from src.services.rag_service import RAGService
from src.utils.logger import logger

APP_NAME = "Semantic Search RAG API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "REST API for document ingestion and semantic retrieval "
    "using a Retrieval-Augmented Generation (RAG) pipeline."
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""

    logger.info("Starting %s...", APP_NAME)

    service = RAGService()
    app.state.rag_service = service

    try:
        yield
    finally:
        logger.info("Shutting down %s...", APP_NAME)

        close = getattr(service, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                logger.exception("Failed to close RAG service.")

        logger.info("Application shutdown complete.")


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
)


@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    exc: ValueError,
) -> JSONResponse:
    logger.warning(
        "Validation error on %s: %s",
        request.url.path,
        exc,
    )

    return JSONResponse(
        status_code=400,
        content=ErrorResponse(detail=str(exc)).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(
        "Request validation error on %s",
        request.url.path,
    )

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(detail="Request validation failed.").model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled exception on %s",
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(detail="Internal server error.").model_dump(),
    )


app.include_router(router)


@app.get(
    "/",
    tags=["System"],
    summary="API Information",
)
async def root() -> dict[str, str]:
    """Return API status."""

    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health Check",
)
async def health() -> dict[str, str]:
    """Simple health endpoint for orchestration systems."""

    return {
        "status": "healthy",
    }
