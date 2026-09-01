# Methodology

## Core hypothesis

Literary syntactic and rhetorical complexity — antithesis, euphemism,
neologism, metaphor, paradox, zeugma, parody, and other phenomena
catalogued during annotation — degrades the semantic fidelity of
embeddings, even when the propositional content of the text is preserved.
We test this by comparing each original literary fragment to an
"intralingual translation" — a syntactically direct rewrite in
contemporary Portuguese that removes the studied phenomenon without
changing what is said.

If the hypothesis holds, the (original, simplified) pair should show a
lower cosine similarity between embeddings of `texto_original` and
`texto_simplificado` for fragments with more pronounced syntactic
complexity — a "spatial drift" effect measured across multiple embedding
architectures (BGE-M3, LaBSE, EmbeddingGemma), so the conclusion doesn't
depend on a single model.

## Intralingual translation protocol

The "intralingual translation" is the pair produced for each original
fragment, and it is the most sensitive input of the experiment: if it isn't
actually equivalent in propositional content, any difference measured in
embedding similarity could reflect content divergence rather than
syntactic complexity itself. The protocol therefore prioritizes semantic
equivalence
over fluency or elegance.

**Goal of the rewrite**: preserve what the text asserts, asks, denies, or
logically implies, while removing the marked linguistic phenomenon
(`fenomeno_linguistico`) — reordering hyperbatic syntax into direct SVO
order, replacing neologisms with a paraphrase in current vocabulary, making
the literal sense behind a metaphor explicit, resolving the apparent
tension of a paradox in direct language.

`fenomeno_linguistico` is recorded as free text, not a fixed category
list: the annotator names whatever phenomenon dominates the fragment. The
pilot dataset already catalogs 12 distinct values with no closed list
enforced — e.g. antithesis, euphemism, cosmic metaphor, neologism, paradox,
parody, zeugma (see `data/processed/dataset_v0.jsonl` for the current set
in use).

**Equivalence check — bidirectional entailment**: before a pair enters the
final dataset, the annotator must be able to assert both directions of
logical implication:

1. `texto_original` entails `texto_simplificado` — nothing was added in the
   simplification that wasn't (even if implicitly) in the original.
2. `texto_simplificado` entails `texto_original` — nothing from the
   original's content was lost or weakened in the simplification.

When the annotator can't confidently support both directions, the pair is
not a "good intralingual translation" — see detailed criteria in
`docs/ANNOTATION_GUIDE.md`. The `nivel_confianca_equivalencia` field
(one of three categories: "alta", "média", "baixa") records confidence in
this bidirectional check.

This protocol is deliberately human-driven at this stage of the project. An
automated entailment check (e.g. via an NLI model or an LLM judge) is a
possible extension to validate already-annotated pairs at scale, but it
does not replace human annotation as the inclusion criterion for the
dataset.

## Embedding Spatial Drift

**Question**: do fragments with higher literary syntactic complexity
produce a lower cosine similarity between `texto_original` and
`texto_simplificado` than syntactically direct fragments — even though both
members of the pair are, by construction, semantically equivalent?

**Design**:
1. Generate embeddings of `texto_original` and `texto_simplificado` for
   each pair, using multiple embedding models (BGE-M3, LaBSE,
   EmbeddingGemma), so the conclusion doesn't depend on a single
   architecture.
2. Compute the cosine similarity between the two vectors of each pair, per
   model.
3. Aggregate similarity by `fenomeno_linguistico` and by author, and
   compare the distributions across phenomena and across models.

**Expected reading under the hypothesis**: pairs whose original is marked
with pronounced hyperbaton, dense neologism, or opaque metaphor should show
systematically lower cosine similarity than pairs whose original is already
syntactically close to the "translation" (a "spatial drift" effect of the
complex fragment relative to its actual propositional content, as measured
in embedding space).

Implemented in `src/embeddings/models.py` (embedding model classes —
BGE-M3, LaBSE, EmbeddingGemma — with a common `encode()` interface),
`src/embeddings/similarity.py` (cosine similarity computation), and
`src/embeddings/run_phase1.py` (the end-to-end pipeline: reads the
dataset, generates embeddings and similarities per model, and writes
`results/phase1_embeddings/cosine_similarity_by_model.csv`).

## Future work / not implemented in this version

An earlier phase of this project ("Phase 2: Interpretive Blindness")
tested a related but separate question: do LLMs make more
interpretation/logical-inference errors — hallucination, reasoning
breakdown, refusal — when processing `texto_original` than when
processing `texto_simplificado` of the same pair, and does that
difference scale with the fragment's literary syntactic complexity? The
design submitted both versions of each pair, separately, to multiple LLMs
(Gemini 2.5 Flash, Qwen3 via local Ollama, Llama 3.3 via Groq), with a
standardized interpretation prompt, then compared failure rates between
versions.

It was piloted with a single model (Qwen3 8B via local Ollama) across all
12 pilot pairs, using a closed true/false question and an open
interpretation question per fragment. The closed-question results showed
no aggregate effect: `qwen3:8b` scored 11/12 (91.7%) on both
`texto_original` and `texto_simplificado`, near-ceiling on both versions
with no room left to distinguish them at this sample size. The instrument
— not necessarily the underlying hypothesis — is the likely reason: a
binary true/false question leaves little room for the kind of subtle
interpretive error the hypothesis predicts, unlike the (never-scored)
open-question responses collected in the same pilot.

This phase was dropped from the project's active scope on that basis: the
measurement instrument used in the pilot proved insensitive to the effect
being studied, and validating a better one (e.g. scoring the open
responses, or building the response-classification pipeline that was
stubbed but never implemented) was judged out of scope for the current,
embeddings-only version of this project. The pilot code, data, and full
results are archived rather than deleted:

- Code: [`archive/src/llm_eval/`](../archive/src/llm_eval/)
- Questions used: [`archive/data/processed/interpretation_questions.jsonl`](../archive/data/processed/interpretation_questions.jsonl)
- Raw responses and full write-up: [`results/archive/phase2_llm_eval/`](../results/archive/phase2_llm_eval/)

## Status

Pilot dataset built and validated at `data/processed/dataset_v0.jsonl` (12
annotated pairs). The embedding pipeline (`src/embeddings/`) is
implemented and has been run on the pilot dataset with all three models;
results in `results/phase1_embeddings/cosine_similarity_by_model.csv`.
This is currently the entire active scope of the project — see "Future
work" above for the discontinued LLM-interpretation pilot.

## References

Grouped by the part of the methodology each one supports.

**Sentence embeddings and semantic similarity** (Embedding Spatial Drift
design):

- Reimers, N. & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings
  using Siamese BERT-Networks*. EMNLP.
- Feng, F. et al. (2022). *Language-agnostic BERT Sentence Embedding*
  (LaBSE). ACL.
- Chen, J. et al. (2024). *BGE-M3: Multi-Lingual, Multi-Functionality,
  Multi-Granularity Text Embeddings*. arXiv:2402.03216.
- Cer, D. et al. (2017). *SemEval-2017 Task 1: Semantic Textual
  Similarity Multilingual and Crosslingual Focused Evaluation*.
  SemEval.

**Geometry of embedding space** (motivates treating cosine drift as
possibly reflecting surface form, not just meaning):

- Ethayarajh, K. (2019). *How Contextual are Contextualized Word
  Representations?*. EMNLP.
- Reif, E. et al. (2019). *Visualizing and Measuring the Geometry of
  BERT*. NeurIPS.

**Natural language inference** (basis for the bidirectional entailment
check in the intralingual translation protocol):

- Bowman, S. R. et al. (2015). *A Large Annotated Corpus for Learning
  Natural Language Inference* (SNLI). EMNLP.
- Williams, A., Nangia, N. & Bowman, S. R. (2018). *A Broad-Coverage
  Challenge Corpus for Sentence Understanding through Inference*
  (MultiNLI). NAACL.

**Paraphrase and text simplification** (basis for treating the
original/simplified pair as a controlled semantic-preservation task):

- Bhagat, R. & Hovy, E. (2013). *What Is a Paraphrase?*. Computational
  Linguistics, 39(3).
- Alva-Manchego, F., Scarton, C. & Specia, L. (2020). *Data-Driven
  Sentence Simplification: Survey and Benchmark*. Computational
  Linguistics, 46(1).

**Figurative language and logical contradiction** (basis for the
"logical-pragmatic" vs. "lexical/rhetorical" phenomenon grouping):

- de Marneffe, M.-C., Rafferty, A. N. & Manning, C. D. (2008). *Finding
  Contradictions in Text*. ACL.
- Shutova, E. (2010). *Automatic Metaphor Interpretation as a
  Paraphrasing Task*. NAACL.

**Pragmatics and context-dependency** (theoretical basis for the
context-dependency classification behind the confound in the Results
section — the strongest and most directly load-bearing citations in this
list):

- Grice, H. P. (1975). *Logic and Conversation*. In Cole, P. & Morgan,
  J. L. (eds.), *Syntax and Semantics 3: Speech Acts*. Academic Press.
- Levinson, S. C. (1983). *Pragmatics*. Cambridge University Press.

**Computational literary stylistics** (motivation — connects to the
project's origin story, see `apresentacao/`):

- Kao, J. & Jurafsky, D. (2012). *A Computational Analysis of Style,
  Affect, and Imagery in Contemporary Poetry*. NAACL Workshop on
  Computational Linguistics for Literature.
- Piper, A., So, R. J. & Bamman, D. (2021). *Narrative Theory for
  Computational Narrative Understanding*. EMNLP.

**Retrieval-augmented generation and chunking** (basis for the "Open
question for future work" in the README):

- Lewis, P. et al. (2020). *Retrieval-Augmented Generation for
  Knowledge-Intensive NLP Tasks*. NeurIPS.
- Karpukhin, V. et al. (2020). *Dense Passage Retrieval for Open-Domain
  Question Answering*. EMNLP.
