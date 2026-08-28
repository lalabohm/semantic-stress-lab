# Semantic Stress Lab

Research on how literary syntactic and rhetorical complexity —
antithesis, euphemism, neologism, paradox, zeugma, parody, and related
phenomena — affects embedding similarity. This project measures how the
syntactic-literary complexity of a fragment affects the embedding
similarity (cosine similarity, a "spatial drift" effect) between an
original text and its "intralingual translation" — a simplified,
semantically equivalent rewrite in contemporary Portuguese — across
multiple embedding models (BGE-M3, LaBSE, EmbeddingGemma), so the
conclusion doesn't depend on a single architecture. This project tests
**Portuguese-language texts specifically**: the corpus is built from
public-domain Brazilian literature (Padre Antônio Vieira, Machado de
Assis, Augusto dos Anjos, Mário de Andrade, Aluísio Azevedo).

**Experiment**: for each (original, simplified) pair, generate embeddings
of `texto_original` and `texto_simplificado` with each model, compute
their cosine similarity, and compare that similarity across
`fenomeno_linguistico` and across models — under the hypothesis, a
fragment with more pronounced syntactic complexity should show lower
similarity than a syntactically direct one, even though both members of
the pair are, by construction, semantically equivalent.

Full methodology, including the intralingual translation protocol and the
bidirectional entailment check, in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).
Annotation criteria in [`docs/ANNOTATION_GUIDE.md`](docs/ANNOTATION_GUIDE.md).

## Current status

✅ Dataset (`data/annotation/dataset_v0_draft.csv`) built, validated, and
converted to `data/processed/dataset_v0.jsonl` via the schema in
`src/dataset/schema.py` (`DatasetEntry`) and `src/dataset/csv_to_jsonl.py`.
Started at 12 annotated pairs (1 per phenomenon) and was **expanded to 25
pairs** to add repeat observations for four phenomena (Paradoxo, Antítese,
Hipérbato, Zeugma) — see [Results](#results-embedding-spatial-drift) for why
that expansion mattered.

✅ The embedding pipeline is implemented in `src/embeddings/` and has been run
twice with all three embedding models (BGE-M3, LaBSE, EmbeddingGemma): once
on the 12-pair pilot
([`results/phase1_embeddings/cosine_similarity_by_model.csv`](results/phase1_embeddings/cosine_similarity_by_model.csv),
preserved for comparison) and once on the expanded 25-pair dataset
([`_v1` suffixed files](results/phase1_embeddings/cosine_similarity_by_model_v1.csv)),
no missing values in either run. A 5-pair synthetic control set
(`data/processed/control_baseline.jsonl`, trivial paraphrases with no
rhetorical figure) was also run through the same pipeline to establish a
similarity floor.

An earlier phase of this project piloted an LLM interpretation-evaluation
experiment; it was dropped from active scope and archived — see
[`archive/`](archive/) and the "Future work" section in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for what it was and why it
was discontinued.

## Results: embedding spatial drift

The results below are presented in the order they were actually found,
including the point where the original hypothesis stopped holding up. This
project treats that as the process working as intended, not as a failure to
report quietly: an initial pattern was proposed from a small sample, tested
against a control and a possible confound, and then re-tested against more
data — which is exactly what turned up a more robust explanation than the
one we started with.

**1. Initial hypothesis and first pattern (n=12, one pair per phenomenon).**
The starting hypothesis was that specific rhetorical/syntactic categories —
paradox, zeugma, antithesis, etc. — would drift by different amounts in
embedding space. The first pilot run seemed to confirm this cleanly:
*Paradoxo* had the lowest cosine similarity of the set (0.34–0.51 across the
three models), *Zeugma* the highest (0.87–0.88), and all three
architecturally unrelated models (BGE-M3, LaBSE, EmbeddingGemma) agreed on
both extremes — a promising sign against single-model artifact.

**2. Control baseline (5 synthetic trivial-paraphrase pairs).** To know
whether that spread was meaningful, we measured a similarity "floor": pairs
that say the same thing with no rhetorical complexity at all scored
0.95–0.97 across models. Converting each phenomenon's similarity to a
z-score against that floor, 11 of the 12 original phenomena deviated far
beyond what sampling noise would explain — real signal, not an artifact of
n=12.

**3. A confound surfaces: context-dependency.** Manual review found that
several fragments depend on context outside the excerpt to be
fully interpretable (presuppositional connectives like "mas ainda",
unresolved deixis, an unidentified interlocutor). Splitting the 12 pairs
by that criterion showed a large, significant gap — context-dependent
fragments averaged 0.57 similarity vs. 0.73 for self-contained ones
(Mann-Whitney p≈0.004) — and 5 of the 6 "logical-pragmatic" phenomena
(including most of the paradox examples) were also context-dependent.
The two variables were almost completely confounded in the 12-pair set:
there was no way yet to tell whether it was the rhetorical figure itself,
or the missing context, doing the work.

**4. Dataset expansion (12 → 25 pairs) breaks the original hierarchy.**
Adding more Paradoxo and Antítese examples (Camões, a second Gregório de
Matos sonnet) was the direct test of that confound. Result: the original
hierarchy did not survive. `matos_001` (Gregório de Matos, *Paradoxo*, but
self-contained) came out with the **highest** average similarity in the
entire 25-pair dataset (0.889) — tied with the best Zeugma example — while
`vieira_002` (Padre Antônio Vieira, *Paradoxo*, context-dependent) remained
the **lowest** (0.393). Same rhetorical label, opposite ends of the
distribution. Being "a paradox" predicts nothing on its own; whether the
excerpt depends on context does.

**5. Ruling out a simpler confound: text length.** Before accepting
context-dependency as the explanation, we checked whether it was just a
proxy for how much the simplified rewrite had to expand to compensate for
what was cut. The raw character-count difference between original and
simplified text was *not* significantly correlated with similarity, but
the *proportional* expansion ratio (simplified length / original length)
was — a moderate negative correlation (r≈−0.43 to −0.47, p<0.05) across
all three models: rewrites that had to expand proportionally more tended
to drift further from the original in embedding space.

**6. Two independent factors, not one.** A multiple regression
(`similaridade ~ razão_tamanho + dependia_contexto`) tested whether these
two variables were really separate effects or whether one was secretly
absorbing the other. Both stayed statistically significant when
controlling for the other in nearly every model/term combination (R²
0.35–0.42), with only one borderline case (EmbeddingGemma's size-ratio
term, p≈0.05). With n=25 and 2 predictors, this is indicative, not
conclusive — but it supports treating context-dependency and proportional
text expansion as two distinct, mostly independent contributors.

**Current working conclusion:** the rhetorical category of a fragment
(paradox, zeugma, antithesis...) does not by itself predict how much an
embedding "drifts" between the original and its simplified rewrite. Two
more fundamental factors do a better job: (a) whether the excerpt depends
on context missing from the recorded fragment, and (b) how much,
proportionally, the simplified rewrite had to expand to compensate for
what was cut. Mean similarity across all 25 pairs, per model, for
reference:

| Model | Mean | Std dev |
|---|---|---|
| BGE-M3 | 0.7612 | 0.1100 |
| LaBSE | 0.7531 | 0.1526 |
| EmbeddingGemma | 0.7112 | 0.1445 |

Full statistical detail (z-scores, the Mann-Whitney tests, the length
correlations, and the regression tables) is in
`results/phase1_embeddings/` and walked through step by step in
`notebooks/exploratory_analysis.ipynb`. With n=25 pairs total, this remains
exploratory/hypothesis-generating rather than confirmatory — the natural
next step is a larger dataset balanced across rhetorical category ×
context-dependency × expansion ratio, so each factor can be tested with
real statistical power.

## Project structure

```
archive/          code and data from the discontinued LLM-interpretation
                  pilot (out of active scope — see docs/METHODOLOGY.md)
assets/           static images (e.g. project photos)
data/
  raw/            extracted original texts, organized by author
  processed/      final consolidated dataset (.jsonl)
  annotation/     working spreadsheets/CSVs for human review
src/
  dataset/        dataset construction and validation (schema, CSV -> JSONL)
  embeddings/     embedding models, cosine similarity, the main pipeline
notebooks/        exploratory analysis
docs/             METHODOLOGY.md, ANNOTATION_GUIDE.md
results/          experiment outputs, plots, tables
tests/            automated tests
```

## Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

EmbeddingGemma (one of the three embedding models) is a gated model:
accept the license at
[google/embeddinggemma-300m](https://huggingface.co/google/embeddinggemma-300m)
and authenticate with `huggingface-cli login` (or set `HF_TOKEN`, see
`.env.example`) before running the pipeline with all three embedding
models.

## How to run

**Build the dataset** from an annotation spreadsheet:

```bash
python -m src.dataset.csv_to_jsonl \
  --input data/annotation/dataset_v0_draft.csv \
  --output data/processed/dataset_v0.jsonl
```

See `data/annotation/exemplo.csv` for the expected column format (one per
field of `DatasetEntry` in `src/dataset/schema.py`). Validation errors are
collected across all rows and reported together; the `.jsonl` file is only
written if every row passes validation.

**Run the tests**:

```bash
pytest
```

**Generate embeddings and compute cosine similarity**:

```bash
# quick smoke test on a single pair first
python -m src.embeddings.run_phase1 --ids vieira_001 --output /tmp/test.csv

# full run
python -m src.embeddings.run_phase1
```

## Open question for future work

The context-dependency finding above has a practical angle worth studying
separately: **do text chunks need to be semantically self-contained to embed
reliably?** Several fragments in this dataset scored low similarity not
because of their rhetorical complexity but because they presuppose context
cut off by the excerpt boundary (an unresolved connective, deixis, an
unidentified interlocutor). That is structurally the same problem a
retrieval/chunking pipeline faces when it splits a document without regard
for whether each chunk stands on its own — so the same effect measured here
on literary fragments may be relevant to how chunk boundaries are chosen in
RAG systems more generally. This hasn't been tested against non-literary
text or against different chunking strategies; it's noted here as a
follow-up question, not a claim.
