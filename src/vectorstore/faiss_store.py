import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from src.config.settings import FAISS_INDEX_PATH, FAISS_METADATA_PATH
from src.embeddings import EmbeddingModel
from src.utils.logger import logger


class FAISSStore:
    def __init__(self):
        self.index_path = Path(FAISS_INDEX_PATH)
        self.metadata_path = Path(FAISS_METADATA_PATH)

        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        # FIX: expose dimension explicitly (required by retriever + validation)
        self.dimension = EmbeddingModel.get_embedding_dimension()

        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata: list[dict[str, Any]] = []

        self.load()

    def add(self, embeddings: np.ndarray, metadata: list[dict[str, Any]]) -> None:
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata count mismatch")

        embeddings = embeddings.astype(np.float32)
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        filter_by: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:

        if self.index.ntotal == 0:
            return []

        query_embedding = query_embedding.astype(np.float32)
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k * 5)

        results = []

        for score, idx in sorted(
            zip(scores[0], indices[0]),
            key=lambda x: x[0],
            reverse=True,
        ):
            if idx == -1:
                continue

            meta = self.metadata[idx]

            if filter_by and not all(meta.get(k) == v for k, v in filter_by.items()):
                continue

            results.append(
                {
                    "score": float(score),
                    "document_id": meta.get("document_id"),
                    "page_number": meta.get("page_number"),
                    "chunk_index": meta.get("chunk_index"),
                    "source_name": meta.get("source_name"),
                    "text": meta.get("text"),
                    "metadata": meta,
                }
            )

            if len(results) >= top_k:
                break

        return results

    def save(self) -> None:
        try:
            faiss.write_index(self.index, str(self.index_path))

            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)

        except Exception:
            logger.exception("Failed to save FAISS store")
            raise

    def load(self) -> None:
        try:
            if self.index_path.exists():
                self.index = faiss.read_index(str(self.index_path))

            if self.metadata_path.exists():
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)

        except Exception:
            logger.exception("Failed to load FAISS store")
            raise
