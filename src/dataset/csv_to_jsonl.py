#!/usr/bin/env python3
"""Converts an annotation spreadsheet (CSV) into the final .jsonl dataset.

Usage:
    python -m src.dataset.csv_to_jsonl \\
        --input data/annotation/lote_01.csv \\
        --output data/processed/dataset.jsonl

The input CSV must have one column per schema field
(`src/dataset/schema.py::FragmentoDataset`): id, autor, obra,
ano_publicacao, fenomeno_linguistico, texto_original, texto_simplificado,
anotador_original, anotador_revisao, nivel_confianca_equivalencia, notas.

Optional columns (ano_publicacao, anotador_revisao, notas) may be left
blank in CSV rows; empty cells are treated as `None`.

Each row is validated against `FragmentoDataset` before being written.
Invalid rows are reported on stderr with the line number and the
validation error, and by default don't stop the conversion of the
remaining rows (use --strict to abort on the first error).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import jsonlines
import pandas as pd
from pydantic import ValidationError

from src.dataset.schema import FragmentoDataset

# Columns that may be left blank in the CSV (mapped to None before validation).
_OPTIONAL_COLUMNS = {"ano_publicacao", "anotador_revisao", "notas"}


def _row_to_record(row: pd.Series) -> dict[str, Any]:
    """Converts a CSV row (pandas Series) into a dict ready for validation."""
    record = row.to_dict()
    for key in _OPTIONAL_COLUMNS:
        value = record.get(key)
        if pd.isna(value) or value == "":
            record[key] = None
    if record.get("ano_publicacao") is not None:
        record["ano_publicacao"] = int(record["ano_publicacao"])
    if record.get("nivel_confianca_equivalencia") is not None and not pd.isna(
        record["nivel_confianca_equivalencia"]
    ):
        record["nivel_confianca_equivalencia"] = int(record["nivel_confianca_equivalencia"])
    return record


def convert(input_path: Path, output_path: Path, strict: bool = False) -> tuple[int, int]:
    """Reads `input_path`, validates each row, and writes valid records to `output_path`.

    Returns (n_valid, n_invalid).
    """
    df = pd.read_csv(input_path, dtype=str)

    missing_columns = set(FragmentoDataset.model_fields) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"input CSV is missing required columns: {sorted(missing_columns)}"
        )

    valid_records: list[FragmentoDataset] = []
    errors: list[str] = []

    for line_number, (_, row) in enumerate(df.iterrows(), start=2):  # +2: header + 1-index
        raw = _row_to_record(row)
        try:
            valid_records.append(FragmentoDataset(**raw))
        except ValidationError as exc:
            message = f"line {line_number} (id={raw.get('id')!r}): {exc}"
            if strict:
                raise ValueError(message) from exc
            errors.append(message)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonlines.open(output_path, mode="w") as writer:
        for record in valid_records:
            writer.write(record.model_dump(mode="json"))

    for message in errors:
        print(f"[WARNING] record discarded — {message}", file=sys.stderr)

    return len(valid_records), len(errors)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, required=True, help="Input annotation CSV.")
    parser.add_argument("--output", type=Path, required=True, help="Output .jsonl path.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Abort on the first invalid row instead of discarding it and continuing.",
    )
    args = parser.parse_args()

    n_valid, n_invalid = convert(args.input, args.output, strict=args.strict)
    print(f"OK: {n_valid} valid record(s) written to {args.output}")
    if n_invalid:
        print(f"WARNING: {n_invalid} record(s) discarded due to validation failure", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
