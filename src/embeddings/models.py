"""Embedding model interfaces for Phase 1 of the Semantic Stress Lab.

Provides a common interface (`EmbeddingModel`) and concrete, lazily-loaded
implementations for the three embedding models used in Phase 1:

    - BGE-M3          (BAAI/bge-m3)
    - LaBSE           (sentence-transformers/LaBSE)
    - EmbeddingGemma  (google/embeddinggemma-300m — gated on Hugging Face;
                        requires accepting Google's license and
                        authenticating, e.g. `huggingface-cli login` or
                        the `HF_TOKEN` env var, before it can be downloaded)

Each model detects CUDA automatically (falls back to CPU) and caches the
underlying `SentenceTransformer` instance after the first call to
`encode()`, so repeated calls don't reload the weights.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import torch
from sentence_transformers import SentenceTransformer


def _detect_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


class EmbeddingModel(ABC):
    """Common interface for embedding models used in Phase 1."""

    name: str

    @abstractmethod
    def encode(self, texto: str) -> np.ndarray:
        """Encodes a single text into a dense embedding vector."""
        raise NotImplementedError


class _SentenceTransformerModel(EmbeddingModel):
    """Base class for embedding models backed by sentence-transformers.

    The underlying `SentenceTransformer` is loaded lazily on the first
    call to `encode()` and cached on the instance (`self._model`), so
    constructing the wrapper is cheap and the (potentially large) model
    weights are only loaded — and only loaded once — when actually needed.
    """

    def __init__(self, model_id: str, name: str, trust_remote_code: bool = False) -> None:
        self._model_id = model_id
        self.name = name
        self._trust_remote_code = trust_remote_code
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            device = _detect_device()
            self._model = SentenceTransformer(
                self._model_id,
                device=device,
                trust_remote_code=self._trust_remote_code,
            )
        return self._model

    def encode(self, texto: str) -> np.ndarray:
        return self.model.encode(texto, convert_to_numpy=True)


class BGEM3Model(_SentenceTransformerModel):
    """BAAI/bge-m3 multilingual embedding model."""

    def __init__(self) -> None:
        super().__init__(model_id="BAAI/bge-m3", name="bge_m3")


class LaBSEModel(_SentenceTransformerModel):
    """sentence-transformers/LaBSE multilingual embedding model."""

    def __init__(self) -> None:
        super().__init__(model_id="sentence-transformers/LaBSE", name="labse")


class EmbeddingGemmaModel(_SentenceTransformerModel):
    """google/embeddinggemma-300m embedding model.

    Gated on Hugging Face: you must accept Google's usage license on the
    model page (https://huggingface.co/google/embeddinggemma-300m) and be
    authenticated (`huggingface-cli login` or `HF_TOKEN` env var) before
    this model can be downloaded. Requires a recent transformers/
    sentence-transformers version with Gemma 3 support.
    """

    def __init__(self) -> None:
        super().__init__(model_id="google/embeddinggemma-300m", name="embeddinggemma")
