#!/usr/bin/env python3
"""Converts an annotation spreadsheet (CSV) into the final .jsonl dataset.

Usage:
    python -m src.dataset.csv_to_jsonl \\
        --input data/annotation/dataset_v0_draft.csv \\
        --output data/processed/dataset_v0.jsonl

The input CSV must have one column per schema field
(`src/dataset/schema.py::DatasetEntry`): id, autor, obra,
ano_publicacao, fenomeno_linguistico, texto_original, texto_simplificado,
nivel_confianca_equivalencia, notas.

`notas` may be left blank in CSV rows.

Every row is validated against `DatasetEntry` before anything is written.
Validation errors are collected for ALL rows (not just the first one) and
reported together; the .jsonl output file is only written if every row
passes validation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import ValidationError

from src.dataset.schema import DatasetEntry


def _row_to_record(row: pd.Series) -> dict[str, Any]:
    """Converts a CSV row (pandas Series) into a dict ready for validation."""
    record = row.to_dict()

    if record.get("ano_publicacao") not in (None, ""):
        record["ano_publicacao"] = int(float(record["ano_publicacao"]))

    return record


def convert(input_path: Path, output_path: Path) -> list[DatasetEntry]:
    """Reads `input_path`, validates every row, and writes `output_path`.

    Raises ValueError (with all collected errors) if any row is invalid;
    in that case, no output file is written. Returns the validated
    records on success.
    """
    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)

    missing_columns = set(DatasetEntry.model_fields) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"input CSV is missing required columns: {sorted(missing_columns)}"
        )

    records: list[DatasetEntry] = []
    errors: list[str] = []

    for line_number, (_, row) in enumerate(df.iterrows(), start=2):  # +2: header + 1-index
        raw = _row_to_record(row)
        try:
            records.append(DatasetEntry(**raw))
        except ValidationError as exc:
            errors.append(f"linha {line_number} (id={raw.get('id')!r}):\n{exc}")

    if errors:
        details = "\n\n".join(errors)
        raise ValueError(
            f"validação falhou em {len(errors)} de {len(df)} linha(s) — "
            f"nenhum arquivo .jsonl foi escrito:\n\n{details}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record.model_dump(mode="json"), ensure_ascii=False))
            f.write("\n")

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, required=True, help="Input annotation CSV.")
    parser.add_argument("--output", type=Path, required=True, help="Output .jsonl path.")
    args = parser.parse_args()

    try:
        records = convert(args.input, args.output)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: {len(records)} registro(s) validado(s) e gravado(s) em {args.output}")


if __name__ == "__main__":
    main()
