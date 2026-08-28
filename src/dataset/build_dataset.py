"""Consolidates multiple annotation batches into a single validated dataset.

TODO: this module is not implemented yet — it's a stub for structure review
before writing the logic.

Planned responsibilities:
    - Discover and read all .jsonl files already converted in
      data/processed/ (one per annotation batch, generated via
      `csv_to_jsonl.py`).
    - Detect duplicate `id`s across batches and decide a resolution policy
      (error? keep the most recent?).
    - Apply aggregate quality filters, e.g.:
        * discard (or flag) records with `nivel_confianca_equivalencia`
          below a configurable threshold (distinguish in-review dataset vs.
          frozen dataset for Phase 1/Phase 2).
    - Write the final consolidated dataset (e.g. data/processed/dataset.jsonl)
      and, possibly, a coverage report by author/linguistic phenomenon to
      guide which gaps still need annotation.

See also:
    - src/dataset/schema.py       (canonical schema / per-record validation)
    - src/dataset/csv_to_jsonl.py (single CSV batch -> JSONL conversion)
    - docs/ANNOTATION_GUIDE.md    (annotation quality criteria)
"""

from __future__ import annotations

# TODO: implement. See module docstring for the planned scope.
