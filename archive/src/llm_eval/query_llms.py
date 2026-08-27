"""Submits texto_original and texto_simplificado to multiple LLMs for interpretation.

TODO: this module is not implemented yet — it's a stub for structure review
before writing the API-calling logic.

Planned responsibilities:
    - Read data/processed/dataset.jsonl.
    - For each fragment (original and simplified, separately, without
      revealing to the model which is which or that a pair exists), send a
      standardized interpretation/logical-inference prompt to each
      configured LLM:
        * Gemini 2.5 Flash  (google-generativeai; GOOGLE_API_KEY)
        * Qwen3             (ollama, local; OLLAMA_HOST)
        * Llama 3.3         (groq; GROQ_API_KEY)
    - Apply appropriate retry/backoff and rate limiting per provider.
    - Persist raw responses (prompt, model, response, timestamp, generation
      parameters) in results/, indexed by fragment `id` + model, so
      `classify_responses.py` doesn't need to re-query the LLMs on every
      run.
    - Load API keys from environment variables (see .env.example), never
      hardcoded.

See also:
    - src/llm_eval/classify_responses.py
    - docs/METHODOLOGY.md, "Phase 2: Interpretive Blindness" section
"""

from __future__ import annotations

# TODO: implement. See module docstring for the planned scope.
