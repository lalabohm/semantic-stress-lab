#!/usr/bin/env python3
"""Phase 2 pilot run: qwen3 interpretation on the 12 pilot pairs.

For each (texto_original, texto_simplificado) pair in
`data/processed/dataset_v0.jsonl`, with the closed/open questions from
`data/processed/interpretation_questions.jsonl`, this script sends 4
prompts to a local qwen3 (via Ollama):

    1. texto_original      + pergunta_fechada
    2. texto_simplificado  + pergunta_fechada
    3. texto_original      + pergunta_aberta
    4. texto_simplificado  + pergunta_aberta

and appends each raw response as one line to
`results/phase2_llm_eval/pilot_qwen3_raw.jsonl`.

This is a data-collection pass only: it does NOT judge whether a
response is correct. That's a manual review step for this first pilot
round (see `src/llm_eval/classify_responses.py` for the planned
automated/hybrid classification stage in a later phase).

Usage
-----
    # Smoke test on a single pair before spending time on all 12:
    python -m src.llm_eval.run_phase2_pilot --ids vieira_001

    # Full pilot run:
    python -m src.llm_eval.run_phase2_pilot
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.llm_eval.ollama_client import DEFAULT_MODEL, ask

_DEFAULT_DATASET = Path("data/processed/dataset_v0.jsonl")
_DEFAULT_QUESTIONS = Path("data/processed/interpretation_questions.jsonl")
_DEFAULT_OUTPUT = Path("results/phase2_llm_eval/pilot_qwen3_raw.jsonl")

# (versao, campo_texto, tipo_pergunta, campo_pergunta)
_TAREFAS = [
    ("original", "texto_original", "fechada", "pergunta_fechada"),
    ("simplificado", "texto_simplificado", "fechada", "pergunta_fechada"),
    ("original", "texto_original", "aberta", "pergunta_aberta"),
    ("simplificado", "texto_simplificado", "aberta", "pergunta_aberta"),
]


def load_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_pairs(dataset: list[dict], questions: list[dict]) -> list[dict]:
    """Joins dataset records with their questions by id, in dataset order."""
    questions_by_id = {q["id"]: q for q in questions}
    pairs = []
    for record in dataset:
        pair_id = record["id"]
        q = questions_by_id.get(pair_id)
        if q is None:
            print(f"  aviso: nenhuma pergunta encontrada para id={pair_id!r}; pulando.", file=sys.stderr)
            continue
        pairs.append({**record, **q})
    return pairs


def run_pilot(pairs: list[dict], output_path: Path, model: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total = len(pairs) * len(_TAREFAS)
    done = 0

    with output_path.open("w", encoding="utf-8") as out:
        for pair in pairs:
            for versao, campo_texto, tipo_pergunta, campo_pergunta in _TAREFAS:
                contexto = pair[campo_texto]
                pergunta = pair[campo_pergunta]
                done += 1
                print(f"[{done}/{total}] id={pair['id']} versao={versao} tipo_pergunta={tipo_pergunta}...", flush=True)

                resposta_modelo = ask(contexto, pergunta, model=model)

                row = {
                    "id": pair["id"],
                    "versao": versao,
                    "tipo_pergunta": tipo_pergunta,
                    "pergunta": pergunta,
                    "resposta_modelo": resposta_modelo,
                    "resposta_esperada_fechada": pair.get("resposta_esperada_fechada") if tipo_pergunta == "fechada" else None,
                    "modelo": model,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()

    print(f"\n{total} resposta(s) salva(s) em: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", type=Path, default=_DEFAULT_DATASET, help="Input .jsonl dataset.")
    parser.add_argument("--questions", type=Path, default=_DEFAULT_QUESTIONS, help="Input .jsonl questions file.")
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT, help="Output .jsonl path for raw responses.")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Ollama model name.")
    parser.add_argument(
        "--ids", type=str, default=None, help="Comma-separated list of pair ids to process (default: all)."
    )
    args = parser.parse_args()

    dataset = load_jsonl(args.dataset)
    questions = load_jsonl(args.questions)

    if args.ids:
        wanted = {x.strip() for x in args.ids.split(",")}
        dataset = [r for r in dataset if r["id"] in wanted]

    pairs = build_pairs(dataset, questions)
    print(f"Processando {len(pairs)} par(es) x {len(_TAREFAS)} tarefa(s) com o modelo '{args.model}'...\n")

    run_pilot(pairs, args.output, args.model)


if __name__ == "__main__":
    main()
