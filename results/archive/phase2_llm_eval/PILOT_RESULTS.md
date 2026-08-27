# Phase 2 pilot results: interpretive blindness (Qwen3 only)

> **Archived.** This was the write-up of the LLM-interpretation pilot when
> it still lived in the main README. The phase was dropped from active
> scope — see the "Future work / not implemented in this version" section
> in [`docs/METHODOLOGY.md`](../../../docs/METHODOLOGY.md) for why. Kept
> here for provenance; not maintained going forward.

For each of the 12 pilot pairs, two hand-written questions were asked
about *both* `texto_original` and `texto_simplificado` (same wording,
same expected answer where applicable) — see
[`archive/data/processed/interpretation_questions.jsonl`](../../../archive/data/processed/interpretation_questions.jsonl):

- a **closed true/false question** about a specific propositional fact,
  objectively checkable and identical for both versions;
- an **open question** asking for an interpretation of the fragment's
  meaning/intention.

All 48 raw responses (`qwen3:8b`, local Ollama) are in
[`pilot_qwen3_raw.jsonl`](pilot_qwen3_raw.jsonl), unclassified — this
pilot round was reviewed manually rather than scored automatically.
Analysis below covers only the 24 closed-question responses; the 24
open-question responses were never analyzed.

| id | fenomeno_linguistico | acertou_original | acertou_simplificado |
|---|---|---|---|
| vieira_001 | Antítese | sim | sim |
| assis_001 | Eufemismo e Ironia | **não** | sim |
| anjos_001 | Metáfora Cósmica / Niilismo Físico | sim | sim |
| anjos_002 | Niilismo Fís / Estática do Nada | sim | **não** |
| anjos_003 | Niilismo Ontológico / Antinomia e Oximoro | sim | sim |
| anjos_004 | Niilismo Ontológico / Não Ser | sim | sim |
| andrade_001 | Neologismo e Sarcasmo | sim | sim |
| anjos_005 | Niilismo Filosófico / Desconstrução Metafísica | sim | sim |
| vieira_002 | Paradoxo | sim | sim |
| andrade_002 | Paródia | sim | sim |
| azevedo_001 | Sugestão e Conotação | sim | sim |
| assis_002 | Zeugma | sim | sim |

- Closed-question accuracy on `texto_original`: **11/12 (91.7%)**
- Closed-question accuracy on `texto_simplificado`: **11/12 (91.7%)**
- Difference: **0 points** — at this sample size (n=12), the aggregate
  closed-question score shows no interpretive blindness effect.

Only two pairs diverge between versions, in opposite directions:

- `assis_001` (**Eufemismo e Ironia**) — wrong on original, correct on
  simplified. This is the signal the hypothesis predicts: the model
  answered "Falso" to the original's euphemism ("...foram estudar a
  geologia dos campos santos"), missing that it means the friends died,
  and only got it right once the simplified version made "morreram e
  foram enterrados" explicit.
- `anjos_002` (**Niilismo Fís / Estática do Nada**) — correct on
  original, wrong on simplified, but for a likely question-design
  artifact rather than a semantic one: the closed question is worded
  around the exact phrase "milhões de mundos", which survives verbatim
  in `texto_original` but was paraphrased to "planetas inteiros" (no
  explicit quantity) in `texto_simplificado`. The model's "Falso" cites
  that literal mismatch. Discounting this pair, the only clean signal in
  this pilot favoring the hypothesis is `assis_001`.

**Reading**: with true/false questions this direct, `qwen3:8b` performed
near-ceiling on both versions in this pilot — too little room for errors
to distinguish original from simplified at n=12. The open-question
responses (never analyzed) would have been the more promising place to
look for a qualitative interpretive-blindness effect, since open answers
have much more room to be subtly wrong than a binary choice does. This is
the reasoning behind dropping the phase from scope rather than continuing
to invest in it: the instrument used, not necessarily the hypothesis, is
what failed to show a signal.
