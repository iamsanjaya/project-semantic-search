"""
FastAPI integration tests for the Retrieval-Augmented Generation (RAG) API.

Run (server must be running):

    python -m tests.test_api
"""

from __future__ import annotations

import os
import sys

import requests

from src.utils.logger import logger

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8002/api/v1")
REQUEST_TIMEOUT = 30

TEST_DOCUMENT = {
    "source_name": "api_test_document.txt",
    "source_type": "text",
    "page_number": 1,
    "text": (
        "Python is a high-level programming language widely used for "
        "artificial intelligence, machine learning, and web development."
    ),
}


def _check_response(response: requests.Response, expected_status: int) -> dict:
    if response.status_code != expected_status:
        raise RuntimeError(
            f"Expected HTTP {expected_status}, "
            f"received {response.status_code}: {response.text}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError("Response is not valid JSON.") from exc


def test_health() -> None:
    response = requests.get(
        f"{BASE_URL}/health",
        timeout=REQUEST_TIMEOUT,
    )

    data = _check_response(response, 200)

    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data

    logger.info("✓ Health endpoint passed")


def test_ingest() -> int:
    response = requests.post(
        f"{BASE_URL}/ingest",
        json=TEST_DOCUMENT,
        timeout=REQUEST_TIMEOUT,
    )

    data = _check_response(response, 201)

    assert data["status"]
    assert isinstance(data["document_id"], int)

    logger.info("✓ Ingest endpoint passed")

    return data["document_id"]


def test_query() -> None:
    payload = {
        "question": "What is Python?",
        "top_k": 3,
    }

    response = requests.post(
        f"{BASE_URL}/query",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    data = _check_response(response, 200)

    assert data["question"]
    assert data["answer"].strip()
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

    logger.info("✓ Query endpoint passed")


def main() -> None:
    logger.info("Running API integration tests...")

    try:
        test_health()
        test_ingest()
        test_query()

    except Exception:
        logger.exception("API integration tests failed.")
        sys.exit(1)

    logger.info("All API integration tests passed.")


if __name__ == "__main__":
    main()
