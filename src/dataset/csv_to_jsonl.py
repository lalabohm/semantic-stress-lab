#!/usr/bin/env python3
"""Converte uma planilha de anotação (CSV) para o dataset final em .jsonl.

Uso:
    python -m src.dataset.csv_to_jsonl \\
        --input data/annotation/lote_01.csv \\
        --output data/processed/dataset.jsonl

O CSV de entrada deve ter uma coluna por campo do schema
(`src/dataset/schema.py::FragmentoDataset`): id, autor, obra,
ano_publicacao, fenomeno_linguistico, texto_original, texto_simplificado,
anotador_original, anotador_revisao, nivel_confianca_equivalencia, notas.

Colunas opcionais (ano_publicacao, anotador_revisao, notas) podem ficar em
branco nas linhas do CSV; células vazias são tratadas como `None`.

Cada linha é validada contra `FragmentoDataset` antes de ser escrita. Linhas
inválidas são reportadas no stderr com o número da linha e o erro de
validação, e por padrão não interrompem a conversão das linhas restantes
(use --strict para abortar no primeiro erro).
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

# Colunas que podem ficar vazias no CSV (mapeadas para None antes da validação).
_OPTIONAL_COLUMNS = {"ano_publicacao", "anotador_revisao", "notas"}


def _row_to_record(row: pd.Series) -> dict[str, Any]:
    """Converte uma linha do CSV (pandas Series) em um dict pronto para validação."""
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
    """Lê `input_path`, valida cada linha e escreve os registros válidos em `output_path`.

    Retorna (n_validos, n_invalidos).
    """
    df = pd.read_csv(input_path, dtype=str)

    missing_columns = set(FragmentoDataset.model_fields) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"CSV de entrada não contém as colunas obrigatórias: {sorted(missing_columns)}"
        )

    valid_records: list[FragmentoDataset] = []
    errors: list[str] = []

    for line_number, (_, row) in enumerate(df.iterrows(), start=2):  # +2: header + 1-index
        raw = _row_to_record(row)
        try:
            valid_records.append(FragmentoDataset(**raw))
        except ValidationError as exc:
            message = f"linha {line_number} (id={raw.get('id')!r}): {exc}"
            if strict:
                raise ValueError(message) from exc
            errors.append(message)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonlines.open(output_path, mode="w") as writer:
        for record in valid_records:
            writer.write(record.model_dump(mode="json"))

    for message in errors:
        print(f"[AVISO] registro descartado — {message}", file=sys.stderr)

    return len(valid_records), len(errors)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, required=True, help="CSV de anotação de entrada.")
    parser.add_argument("--output", type=Path, required=True, help="Caminho do .jsonl de saída.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Aborta na primeira linha inválida em vez de descartá-la e seguir.",
    )
    args = parser.parse_args()

    n_valid, n_invalid = convert(args.input, args.output, strict=args.strict)
    print(f"OK: {n_valid} registro(s) válido(s) escrito(s) em {args.output}")
    if n_invalid:
        print(f"AVISO: {n_invalid} registro(s) descartado(s) por falha de validação", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
