"""Cosine similarity utilities for Phase 1 embedding comparisons."""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cosine


def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Computes cosine similarity between two embedding vectors.

    `scipy.spatial.distance.cosine` returns cosine *distance*
    (1 - cosine_similarity), so the result is converted back to a
    similarity here.
    """
    distance = cosine(vec1, vec2)
    return 1.0 - float(distance)
