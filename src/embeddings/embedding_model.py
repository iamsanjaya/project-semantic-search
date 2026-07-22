from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config.settings import EMBEDDING_MODEL


class EmbeddingModel:
    """
    Singleton wrapper around SentenceTransformer.

    The model and its embedding dimension are lazily loaded and cached
    for the lifetime of the application.
    """

    _model: SentenceTransformer | None = None
    _dimension: int | None = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """
        Return the singleton SentenceTransformer instance.
        """

        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL)

        return cls._model

    @classmethod
    def encode(
        cls,
        texts: str | Sequence[str],
    ) -> np.ndarray:
        """
        Generate normalized embeddings for one or more texts.
        """

        model = cls.get_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.astype(np.float32)

    @classmethod
    def get_embedding_dimension(cls) -> int:
        """
        Return the embedding dimension of the configured model.
        The value is computed once and then cached.
        """

        if cls._dimension is None:
            model = cls.get_model()

            dimension = model.get_embedding_dimension()

            if dimension is None:
                raise ValueError("Unable to determine embedding dimension.")

            cls._dimension = dimension

        return cls._dimension
