"""Minimal client for querying a local Qwen3 model via Ollama.

Wraps the `ollama` Python package (see requirements.txt) to send a piece
of context text (texto_original or texto_simplificado) plus a question,
and return the model's raw response text. Does not classify, score, or
otherwise interpret the response — see the module docstring in
`classify_responses.py` for that stage.

Requires a running local Ollama server with the model already pulled,
e.g.:

    ollama pull qwen3

Set OLLAMA_HOST in .env (see .env.example) if Ollama isn't running on its
default local address.
"""

from __future__ import annotations

import os

import ollama
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "qwen3:8b"  # local tag actually pulled; override with --model if yours differs
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

_PROMPT_TEMPLATE = """Leia atentamente o texto abaixo e responda à pergunta que vem em seguida, baseando-se exclusivamente no que está escrito no texto.

TEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""


def build_prompt(contexto: str, pergunta: str) -> str:
    return _PROMPT_TEMPLATE.format(contexto=contexto.strip(), pergunta=pergunta.strip())


def ask(contexto: str, pergunta: str, model: str = DEFAULT_MODEL, host: str | None = None) -> str:
    """Sends `contexto` + `pergunta` to the model and returns its response text."""
    client = ollama.Client(host=host or DEFAULT_HOST)
    prompt = build_prompt(contexto, pergunta)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    # Quick manual smoke test: `python -m src.llm_eval.ollama_client`
    exemplo = ask(
        contexto="O céu estava azul e não havia nenhuma nuvem à vista.",
        pergunta="O céu estava nublado? (Responda apenas Verdadeiro ou Falso, com uma breve justificativa.)",
    )
    print(exemplo)
