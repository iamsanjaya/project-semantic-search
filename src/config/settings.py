from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ==================================================
# Environment
# ==================================================

load_dotenv()

# ==================================================
# Base Paths
# ==================================================

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Path = BASE_DIR / "data"
FAISS_DIR: Path = DATA_DIR / "faiss"


# ==================================================
# Environment Helpers
# ==================================================


def get_required_env(name: str) -> str:
    """
    Return a required environment variable.

    Raises:
        RuntimeError: If the variable is missing or empty.
    """
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value.strip()


def get_int_env(
    name: str,
    default: int,
    *,
    minimum: int | None = None,
) -> int:
    value = os.getenv(name)

    if value is None:
        result = default
    else:
        try:
            result = int(value)
        except ValueError as exc:
            raise RuntimeError(
                f"Environment variable '{name}' must be an integer."
            ) from exc

    if minimum is not None and result < minimum:
        raise RuntimeError(f"Environment variable '{name}' must be >= {minimum}.")

    return result


def get_float_env(
    name: str,
    default: float,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    value = os.getenv(name)

    if value is None:
        result = default
    else:
        try:
            result = float(value)
        except ValueError as exc:
            raise RuntimeError(
                f"Environment variable '{name}' must be a float."
            ) from exc

    if minimum is not None and result < minimum:
        raise RuntimeError(f"Environment variable '{name}' must be >= {minimum}.")

    if maximum is not None and result > maximum:
        raise RuntimeError(f"Environment variable '{name}' must be <= {maximum}.")

    return result


# ==================================================
# Database
# ==================================================

DATABASE_URL: str = get_required_env("DATABASE_URL")

# ==================================================
# Embeddings
# ==================================================

EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
).strip()

# ==================================================
# Vector Store
# ==================================================

FAISS_INDEX_PATH: str = os.getenv(
    "FAISS_INDEX_PATH",
    str(FAISS_DIR / "faiss.index"),
)

FAISS_METADATA_PATH: str = os.getenv(
    "FAISS_METADATA_PATH",
    str(FAISS_DIR / "metadata.json"),
)

# ==================================================
# Chunking
# ==================================================

CHUNK_SIZE: int = get_int_env(
    "CHUNK_SIZE",
    500,
    minimum=1,
)

CHUNK_OVERLAP: int = get_int_env(
    "CHUNK_OVERLAP",
    100,
    minimum=0,
)

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise RuntimeError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE.")

# ==================================================
# LLM
# ==================================================

GROQ_API_KEY: str = get_required_env("GROQ_API_KEY")

GROQ_MODEL: str = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
).strip()

GROQ_TIMEOUT: int = get_int_env(
    "GROQ_TIMEOUT",
    30,
    minimum=1,
)

GROQ_TEMPERATURE: float = get_float_env(
    "GROQ_TEMPERATURE",
    0.0,
    minimum=0.0,
    maximum=2.0,
)
