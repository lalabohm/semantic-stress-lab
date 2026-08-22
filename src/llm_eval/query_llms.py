"""Submete texto_original e texto_simplificado a múltiplos LLMs para interpretação.

TODO: este módulo ainda não está implementado — é um stub para revisão de
estrutura antes de escrever a lógica de chamada às APIs.

Responsabilidades previstas:
    - Ler data/processed/dataset.jsonl.
    - Para cada fragmento (original e simplificado, separadamente, sem
      revelar ao modelo qual é qual nem que existe um par), enviar um
      prompt padronizado de interpretação/inferência lógica para cada um
      dos LLMs configurados:
        * Gemini 2.5 Flash  (google-generativeai; GOOGLE_API_KEY)
        * Qwen3             (ollama, local; OLLAMA_HOST)
        * Llama 3.3         (groq; GROQ_API_KEY)
    - Aplicar retry/backoff e rate limiting apropriados a cada provedor.
    - Persistir as respostas cruas (prompt, modelo, resposta, timestamp,
      parâmetros de geração) em results/, indexadas por `id` do fragmento
      + modelo, para que `classify_responses.py` não precise re-consultar
      os LLMs a cada execução.
    - Carregar as chaves de API a partir de variáveis de ambiente (ver
      .env.example), nunca hardcoded.

Ver também:
    - src/llm_eval/classify_responses.py
    - docs/METHODOLOGY.md, seção "Fase 2: Cegueira Interpretativa"
"""

from __future__ import annotations

# TODO: implementar. Ver docstring do módulo para o escopo previsto.
