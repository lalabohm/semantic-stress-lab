#!/usr/bin/env python3
"""Generates the Phase 2 interpretation questions for the pilot dataset.

For each (texto_original, texto_simplificado) pair in
`data/processed/dataset_v0.jsonl`, this module defines two hand-written
questions that will be asked, unchanged, about *both* versions of the
fragment:

    a) `pergunta_fechada` — a closed true/false question about a specific
       propositional fact in the fragment. Because texto_original and
       texto_simplificado are annotated as semantically equivalent, the
       correct answer must be identical for both versions.
    b) `pergunta_aberta` — an open question asking for an interpretation
       of the fragment's meaning/intention.

The questions are content, not derived data — they are authored by hand
per pair in `QUESTIONS` below, not generated programmatically from the
text. This module's only job is to pair them with the dataset (pulling
`autor`/`fenomeno_linguistico` for readability) and write them to
`data/processed/interpretation_questions.jsonl` for manual review/editing
before any model is queried.

`run_phase2_pilot.py` reads its questions from that JSONL file, not from
`QUESTIONS` directly — so editing the JSONL after generation is the
intended workflow, and re-running this script would overwrite those edits.

Usage
-----
    # Preview a single pair before committing to the full set:
    python -m src.llm_eval.questions --ids vieira_001

    # Full run (all pairs present in QUESTIONS):
    python -m src.llm_eval.questions
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_DEFAULT_INPUT = Path("data/processed/dataset_v0.jsonl")
_DEFAULT_OUTPUT = Path("data/processed/interpretation_questions.jsonl")

# Suffix appended to every closed question so the answer format is
# unambiguous to the model, without run_phase2_pilot.py or
# ollama_client.py needing to know a question is "closed" vs. "open".
_SUFIXO_FECHADA = " (Responda apenas Verdadeiro ou Falso, com uma breve justificativa.)"

# id -> {pergunta_fechada, resposta_esperada_fechada, pergunta_aberta}
# resposta_esperada_fechada is the human-judged ground truth ("verdadeiro"
# or "falso"), kept here only as a reference for manual review — it is
# not used for any automatic classification.
QUESTIONS: dict[str, dict[str, str]] = {
    "vieira_001": {
        "pergunta_fechada": (
            "De acordo com o trecho, o maior sofrimento relatado pelo autor foi vivido "
            "no mesmo lugar para onde ele está prestes a retornar." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Qual é o sentido da comparação que o autor faz entre o sofrimento anterior "
            "dos pregadores do Evangelho em geral e o sofrimento vivido no lugar mencionado "
            "no trecho? O que essa comparação sugere sobre a atitude do autor diante de "
            "voltar a esse lugar?"
        ),
    },
    "assis_001": {
        "pergunta_fechada": (
            "De acordo com o trecho, todos os amigos antigos do narrador morreram." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "O que o narrador quer dizer, de fato, quando descreve o destino de seus "
            "amigos antigos nesse trecho? Que tom (por exemplo, sério, irônico, "
            "melancólico) essa forma de descrever a morte sugere?"
        ),
    },
    "anjos_001": {
        "pergunta_fechada": (
            "De acordo com o trecho, o eu lírico ouve algo que soa como se viesse de "
            "dentro da Terra." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "O que o eu lírico está descrevendo ao dizer que ouve 'o choro da Energia "
            "abandonada'? O que essa imagem sugere sobre a relação entre o eu lírico e "
            "o mundo físico ao seu redor?"
        ),
    },
    "anjos_002": {
        "pergunta_fechada": (
            "De acordo com o trecho, a força ou energia descrita seria capaz de mover "
            "milhões de mundos, mas permanece parada." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Que ideia o trecho comunica sobre a relação entre potência (capacidade de "
            "ação) e inércia (a força parada, não utilizada)? O que essa contradição "
            "sugere sobre o sentimento expresso no trecho?"
        ),
    },
    "anjos_003": {
        "pergunta_fechada": (
            "De acordo com o trecho, o ser descrito foi gerado a partir do sistema "
            "nervoso do eu lírico." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Que sentimento o eu lírico expressa em relação ao ser a quem se dirige "
            "nesse trecho, e como a forma de descrevê-lo (como mistura de matéria "
            "biológica, fruto de uma força geradora) constrói esse sentimento?"
        ),
    },
    "anjos_004": {
        "pergunta_fechada": (
            "De acordo com o trecho, o eu lírico deseja que o ser a quem se dirige "
            "permaneça morto e esquecido." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Que atitude o eu lírico expressa em relação à morte e ao não-ser nesse "
            "trecho? Esse desejo parece ser de crueldade, de resignação, de alívio, ou "
            "outra coisa? Justifique com base no trecho."
        ),
    },
    "andrade_001": {
        "pergunta_fechada": (
            "De acordo com o trecho, o eu lírico expressa admiração pelo burguês e "
            "pelas aristocracias." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "falso",
        "pergunta_aberta": (
            "Qual é a atitude do eu lírico em relação ao burguês e às aristocracias "
            "nesse trecho, e o que as expressões usadas para descrevê-los revelam "
            "sobre essa atitude?"
        ),
    },
    "anjos_005": {
        "pergunta_fechada": (
            "De acordo com o trecho, o homem a quem o eu lírico se dirige encontrou um "
            "sentido ou verdade absoluta ao analisar o mundo." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "falso",
        "pergunta_aberta": (
            "Que julgamento o eu lírico faz sobre o esforço de reflexão filosófica do "
            "homem a quem se dirige nesse trecho? O que o resultado dessa reflexão, "
            "como descrito no trecho, sugere sobre a visão de mundo expressa aqui?"
        ),
    },
    "vieira_002": {
        "pergunta_fechada": (
            "De acordo com o trecho, a pregação do Evangelho deve seguir regras fixas "
            "e rígidas, aplicadas da mesma forma em qualquer lugar." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "falso",
        "pergunta_aberta": (
            "O que o trecho quer dizer ao afirmar que semear/pregar 'é uma arte sem "
            "arte'? Que ideia sobre a natureza da pregação essa expressão comunica?"
        ),
    },
    "andrade_002": {
        "pergunta_fechada": (
            "De acordo com o trecho, Macunaíma nasceu no interior de uma floresta." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Que papel ou significado o trecho atribui à personagem Macunaíma em "
            "relação ao povo brasileiro? O que isso sugere sobre a intenção da obra ao "
            "apresentar essa personagem logo em sua primeira frase?"
        ),
    },
    "azevedo_001": {
        "pergunta_fechada": (
            "De acordo com o trecho, Miranda sentiu um forte desejo sexual." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "O que o trecho sugere sobre o caráter de Miranda, além do estado físico "
            "descrito? Que outros traços de personalidade são atribuídos a ele, e como "
            "eles se relacionam com o desejo descrito?"
        ),
    },
    "assis_002": {
        "pergunta_fechada": (
            "De acordo com o trecho, Rubião usava um enfeite de seda preta na cabeça." + _SUFIXO_FECHADA
        ),
        "resposta_esperada_fechada": "verdadeiro",
        "pergunta_aberta": (
            "Que impressão geral sobre a aparência e o estado de espírito de Rubião o "
            "trecho constrói, considerando em conjunto as roupas, o gorro e a expressão "
            "descritos?"
        ),
    },
}


def load_dataset(input_path: Path) -> list[dict]:
    records = []
    with input_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_question_records(dataset: list[dict]) -> list[dict]:
    """Joins QUESTIONS with dataset metadata, in dataset order.

    Dataset ids without a matching entry in QUESTIONS are skipped (with a
    warning on stderr) rather than aborting the run, so the module can be
    used to preview a subset (e.g. via --ids) before all 12 pairs are
    authored.
    """
    rows = []
    for record in dataset:
        pair_id = record["id"]
        questions = QUESTIONS.get(pair_id)
        if questions is None:
            print(f"  aviso: nenhuma pergunta definida ainda para id={pair_id!r}; pulando.", file=sys.stderr)
            continue
        rows.append(
            {
                "id": pair_id,
                "autor": record["autor"],
                "fenomeno_linguistico": record["fenomeno_linguistico"],
                "pergunta_fechada": questions["pergunta_fechada"],
                "resposta_esperada_fechada": questions["resposta_esperada_fechada"],
                "pergunta_aberta": questions["pergunta_aberta"],
            }
        )
    return rows


def write_questions_jsonl(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, default=_DEFAULT_INPUT, help="Input .jsonl dataset.")
    parser.add_argument("--output", type=Path, default=_DEFAULT_OUTPUT, help="Output .jsonl path for the questions.")
    parser.add_argument(
        "--ids", type=str, default=None, help="Comma-separated list of ids to process (default: all in QUESTIONS)."
    )
    args = parser.parse_args()

    dataset = load_dataset(args.input)
    if args.ids:
        wanted = {x.strip() for x in args.ids.split(",")}
        dataset = [r for r in dataset if r["id"] in wanted]

    rows = build_question_records(dataset)
    write_questions_jsonl(rows, args.output)

    print(f"{len(rows)} pergunta(s) escrita(s) em: {args.output}\n")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
