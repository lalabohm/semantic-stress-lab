#!/usr/bin/env python3
"""Phase 1 of the Semantic Stress Lab: embedding spatial drift.

HYPOTHESIS
----------
Each record in the dataset pairs a literary fragment marked by a dominant
rhetorical/syntactic phenomenon (antithesis, euphemism, neologism,
paradox, cosmic metaphor, etc.) with an "intralingual translation" —
a rewrite intended to preserve the exact same propositional content while
removing that phenomenon's syntactic complexity. Because both texts are
meant to be semantically equivalent, a good embedding model — one that
represents *meaning* rather than *surface form* — should place them close
together in vector space, regardless of how syntactically different they
are on the surface.

This script tests that assumption empirically: for each
(texto_original, texto_simplificado) pair, it generates embeddings with
three architecturally different models (BGE-M3, LaBSE, EmbeddingGemma)
and computes the cosine similarity between the two vectors of each pair.

INTERPRETATION
---------------
- LOW cosine similarity is evidence of "semantic stress": the embedding
  space is being driven more than it should be by surface syntax (lexical
  choice, sentence structure, register) rather than by the underlying
  propositional content, even though a human annotator judged the pair
  semantically equivalent.
- HIGH cosine similarity is evidence that the model captures deep
  semantic equivalence despite the syntactic complexity of the original —
  i.e. it is robust to the literary phenomenon being tested.

Comparing across three models (and, descriptively, across
`fenomeno_linguistico` categories) helps distinguish a model-specific
quirk from a more general property of embedding spaces.

Usage
-----
    # Quick smoke test on a single pair before spending time/resources on
    # the full dataset:
    python -m src.embeddings.run_phase1 --ids vieira_001 --output /tmp/test.csv

    # Full run:
    python -m src.embeddings.run_phase1
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

from src.embeddings.models import BGEM3Model, EmbeddingGemmaModel, EmbeddingModel, LaBSEModel
from src.embeddings.similarity import compute_cosine_similarity

_DEFAULT_INPUT = Path("data/processed/dataset_v0.jsonl")
_DEFAULT_OUTPUT = Path("results/phase1_embeddings/cosine_similarity_by_model.csv")

# (column suffix, model class) — the suffix is used to build the
# "similaridade_<suffix>" column names in the output CSV.
_MODEL_SPECS: list[tuple[str, type[EmbeddingModel]]] = [
    ("bge_m3", BGEM3Model),
    ("labse", LaBSEModel),
    ("embeddinggemma", EmbeddingGemmaModel),
]


def load_records(input_path: Path) -> list[dict]:
    records = []
    with input_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_models() -> dict[str, EmbeddingModel]:
    """Instantiates and warms up each configured model.

    A model that fails to load (missing weights, no VRAM, gated
    repository without authentication, wrong model id, etc.) is reported
    on stderr and simply excluded from the returned dict — the caller
    treats its similarity column as unavailable (NaN) rather than
    aborting the whole run.
    """
    loaded: dict[str, EmbeddingModel] = {}
    for suffix, cls in _MODEL_SPECS:
        print(f"Carregando modelo '{suffix}'...", flush=True)
        try:
            model = cls()
            model.encode("teste de carregamento")  # forces the lazy load now, fail fast
            loaded[suffix] = model
            print(f"  OK: '{suffix}' carregado com sucesso.", flush=True)
        except Exception as exc:  # noqa: BLE001 - each backend can fail in different, unpredictable ways
            print(f"  ERRO ao carregar modelo '{suffix}': {exc}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print(f"  -> pulando '{suffix}'; os outros modelos continuam normalmente.\n", file=sys.stderr)
    return loaded


def compute_similarities(records: list[dict], models: dict[str, EmbeddingModel]) -> pd.DataFrame:
    rows = []
    for record in records:
        row: dict[str, object] = {
            "id": record["id"],
            "autor": record["autor"],
            "fenomeno_linguistico": record["fenomeno_linguistico"],
            "nivel_confianca_equivalencia": record["nivel_confianca_equivalencia"],
        }
        for suffix, _ in _MODEL_SPECS:
            col = f"similaridade_{suffix}"
            model = models.get(suffix)
            if model is None:
                row[col] = np.nan
                continue
            try:
                vec_orig = model.encode(record["texto_original"])
                vec_simp = model.encode(record["texto_simplificado"])
                row[col] = compute_cosine_similarity(vec_orig, vec_simp)
            except Exception as exc:  # noqa: BLE001
                print(f"  ERRO ao processar id={record['id']!r} com modelo '{suffix}': {exc}", file=sys.stderr)
                row[col] = np.nan

        summary = ", ".join(
            f"{suffix}={row[f'similaridade_{suffix}']:.4f}"
            if not pd.isna(row[f"similaridade_{suffix}"])
            else f"{suffix}=N/A"
            for suffix, _ in _MODEL_SPECS
        )
        print(f"  {row['id']}: {summary}", flush=True)
        rows.append(row)
    return pd.DataFrame(rows)


def print_summary(df: pd.DataFrame) -> None:
    sim_cols = [f"similaridade_{suffix}" for suffix, _ in _MODEL_SPECS]

    print("\n=== Resumo geral (média ± desvio padrão por modelo) ===")
    for col in sim_cols:
        if df[col].notna().any():
            print(f"{col}: {df[col].mean():.4f} +/- {df[col].std():.4f}  (n={df[col].notna().sum()})")
        else:
            print(f"{col}: sem dados (modelo indisponível ou todas as chamadas falharam)")

    print("\n=== Média por fenomeno_linguistico (por modelo) ===")
    grouped = df.groupby("fenomeno_linguistico")[sim_cols].mean()
    with pd.option_context("display.max_rows", None, "display.width", 120):
        print(grouped.to_string(float_format=lambda x: f"{x:.4f}"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, default=_DEFAULT_INPUT, help="Input .jsonl dataset.")
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT, help="Output .csv path.")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N records (smoke test).")
    parser.add_argument(
        "--ids", type=str, default=None, help="Comma-separated list of ids to process (overrides --limit)."
    )
    args = parser.parse_args()

    records = load_records(args.input)

    if args.ids:
        wanted = {x.strip() for x in args.ids.split(",")}
        records = [r for r in records if r["id"] in wanted]
    elif args.limit is not None:
        records = records[: args.limit]

    print(f"Processando {len(records)} par(es) de {args.input}...\n")

    models = load_models()
    if not models:
        print("ERRO: nenhum modelo pôde ser carregado. Abortando.", file=sys.stderr)
        sys.exit(1)

    print()
    df = compute_similarities(records, models)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"\nCSV salvo em: {args.output}")

    print_summary(df)


if __name__ == "__main__":
    main()
