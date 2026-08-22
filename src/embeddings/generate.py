"""Generates embeddings for the dataset's (texto_original, texto_simplificado) pairs.

TODO: this module is not implemented yet — it's a stub for structure review
before writing the model-calling logic.

Planned responsibilities:
    - Read data/processed/dataset.jsonl (format validated by
      src/dataset/schema.py::FragmentoDataset).
    - For each configured embedding model — deliberately more than one, so
      Phase 1 results don't depend on a single embedding architecture —
      generate the vector for `texto_original` and for
      `texto_simplificado`:
        * BGE-M3         (via sentence-transformers)
        * LaBSE          (via sentence-transformers)
        * EmbeddingGemma (via sentence-transformers, when available)
    - Persist embeddings reproducibly (e.g. one .parquet or .npz per model
      in results/, indexed by fragment `id`), so `compare.py` doesn't need
      to recompute embeddings on every run.
    - Record provenance metadata (model name/version, vector dimension,
      timestamp) alongside the vectors.

See also:
    - src/embeddings/compare.py (cosine similarity computation from the
      embeddings generated here)
    - docs/METHODOLOGY.md, "Phase 1: Embedding Spatial Drift" section
"""

from __future__ import annotations

# TODO: implement. See module docstring for the planned scope.
