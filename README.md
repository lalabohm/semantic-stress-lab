# Semantic Stress Lab

Adversarial research on how literary syntactic complexity — antithesis,
euphemism, neologism, paradox, zeugma, parody, and related rhetorical
phenomena — degrades embedding fidelity and induces hallucination /
reasoning breakdown in LLMs during interpretation tasks (RAG). This
project tests **Portuguese-language texts specifically**: the corpus is
built from public-domain Brazilian literature (Padre Antônio Vieira,
Machado de Assis, Augusto dos Anjos, Mário de Andrade, Aluísio Azevedo),
pairing each original fragment with an "intralingual translation" — a
simplified, semantically equivalent rewrite in contemporary Portuguese.

The experiment runs in two phases:

- **Phase 1 — Embedding Spatial Drift**: compares the cosine similarity
  between original and simplified fragments using multiple embedding
  models (BGE-M3, LaBSE, EmbeddingGemma), so results don't depend on a
  single architecture.
- **Phase 2 — Interpretive Blindness**: submits original and simplified
  fragments to multiple LLMs (Gemini 2.5 Flash, Qwen3 via local Ollama,
  Llama 3.3 via Groq) and classifies the responses to detect hallucination
  or reasoning breakdown induced by syntactic complexity.

Full methodology, including the intralingual translation protocol and the
bidirectional entailment check, in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).
Annotation criteria in [`docs/ANNOTATION_GUIDE.md`](docs/ANNOTATION_GUIDE.md).

## Current status

✅ Pilot dataset (`data/annotation/dataset_v0_draft.csv`, 12 annotated
pairs) built, validated, and converted to
`data/processed/dataset_v0.jsonl` via the schema in
`src/dataset/schema.py` (`DatasetEntry`) and
`src/dataset/csv_to_jsonl.py`.

✅ **Phase 1** implemented in `src/embeddings/` and run on the pilot
dataset. Results in
[`results/phase1_embeddings/cosine_similarity_by_model.csv`](results/phase1_embeddings/cosine_similarity_by_model.csv).
BGE-M3 and LaBSE similarities are complete for all 12 pairs;
EmbeddingGemma is gated on Hugging Face and pending authentication
(`huggingface-cli login` after accepting the license at
[google/embeddinggemma-300m](https://huggingface.co/google/embeddinggemma-300m)).

🚧 **Phase 2** (LLM evaluation, `src/llm_eval/`) not started yet — still
stubs.

## Project structure

```
assets/           static images (e.g. project photos)
data/
  raw/            extracted original texts, organized by author
  processed/      final consolidated dataset, in .jsonl
  annotation/     working spreadsheets/CSVs for human review
src/
  dataset/        dataset construction and validation (schema, CSV -> JSONL)
  embeddings/     embedding models, cosine similarity, Phase 1 pipeline
  llm_eval/       LLM calls and response classification (Phase 2) — stub
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

Configure the API keys needed for Phase 2:

```bash
cp .env.example .env
# edit .env with GOOGLE_API_KEY and GROQ_API_KEY
```

Qwen3 runs locally via [Ollama](https://ollama.com/) — no key required, but
the service must be running (`ollama serve`) and the model pulled
(`ollama pull qwen3`).

EmbeddingGemma (used in Phase 1) is a gated model: accept the license at
[google/embeddinggemma-300m](https://huggingface.co/google/embeddinggemma-300m)
and authenticate with `huggingface-cli login` (or set `HF_TOKEN`) before
running Phase 1 with all three embedding models.

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

**Generate embeddings and compute cosine similarity** (Phase 1):

```bash
# quick smoke test on a single pair first
python -m src.embeddings.run_phase1 --ids vieira_001 --output /tmp/test.csv

# full run
python -m src.embeddings.run_phase1
```

**Run LLM evaluation** (Phase 2): not yet implemented — see the TODOs in
`src/llm_eval/query_llms.py` and `src/llm_eval/classify_responses.py`.

---

![Study authors](assets/autores.jpeg)

*Study authors*
