# Archive

Code and data from project phases no longer in active scope. Kept for
provenance and possible future reuse — not maintained, and not covered by
`requirements.txt` guarantees (some imports here may need dependencies
no longer required by the active project).

- `src/llm_eval/` — the "Phase 2: Interpretive Blindness" pilot (question
  generation, an Ollama client, the pilot runner, and unimplemented
  stubs for multi-model querying and response classification). See the
  "Future work / not implemented in this version" section in
  [`docs/METHODOLOGY.md`](../docs/METHODOLOGY.md) for why this was
  dropped from scope, and
  [`results/archive/phase2_llm_eval/PILOT_RESULTS.md`](../results/archive/phase2_llm_eval/PILOT_RESULTS.md)
  for the pilot's results.
- `data/processed/interpretation_questions.jsonl` — the closed/open
  interpretation questions used by that pilot.
