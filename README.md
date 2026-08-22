# Semantic Stress Lab

Adversarial research on how literary syntactic complexity — hyperbaton,
neologism, metaphor, paradox — degrades embedding fidelity and induces
hallucination / reasoning breakdown in LLMs during interpretation tasks
(RAG). This project tests **Portuguese-language texts specifically**: the
corpus is built from public-domain Brazilian and Portuguese literature
(Camões, Padre Antônio Vieira, Gregório de Matos, Mário de Andrade,
Fernando Pessoa and his heteronyms), pairing each original fragment with an
"intralingual translation" — a simplified, semantically equivalent
rewrite in contemporary Portuguese.

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

🚧 Dataset construction phase. The schema (`src/dataset/schema.py`) and the
CSV → JSONL converter (`src/dataset/csv_to_jsonl.py`) are implemented and
tested. Embedding generation and LLM-calling logic
(`src/embeddings/`, `src/llm_eval/`) are still stubs — Phases 1 and 2
haven't been run yet.

## Project structure

```
data/
  raw/            extracted original texts, organized by author
  processed/      final consolidated dataset, in .jsonl
  annotation/     working spreadsheets/CSVs for human review
src/
  dataset/        dataset construction and validation (schema, CSV -> JSONL)
  embeddings/     embedding generation and comparison (Phase 1) — stub
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

## How to run

**Build the dataset** from an annotation spreadsheet:

```bash
python -m src.dataset.csv_to_jsonl \
  --input data/annotation/lote_01.csv \
  --output data/processed/dataset.jsonl
```

See `data/annotation/exemplo.csv` for the expected column format (one per
field of `FragmentoDataset` in `src/dataset/schema.py`).

**Run the tests**:

```bash
pytest
```

**Generate embeddings** (Phase 1) and **run LLM evaluation** (Phase 2): not
yet implemented — see the TODOs in `src/embeddings/generate.py`,
`src/embeddings/compare.py`, `src/llm_eval/query_llms.py`, and
`src/llm_eval/classify_responses.py`.
