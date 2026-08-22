# Annotation Guide

> Initial skeleton — criteria to be refined during the pilot annotation
> round. See `docs/METHODOLOGY.md` for the intralingual translation
> protocol and the bidirectional entailment check this guide
> operationalizes.

## What the annotator is producing

For each selected original fragment (`texto_original`), the annotator
writes an **intralingual translation** (`texto_simplificado`): a rewrite in
contemporary Portuguese that removes the marked `fenomeno_linguistico`
(hyperbaton, neologism, metaphor, or paradox) while preserving the
propositional content of the original — what it asserts, denies, asks, or
implies.

The goal is **not** to produce an elegant paraphrase or a "literary
modernization." It's to produce the most direct, syntactically neutral text
that still says exactly the same thing as the original.

## Criteria for a good intralingual translation

- [ ] **Bidirectional propositional equivalence**: the original entails the
      simplification and the simplification entails the original (no
      content added or lost). See "bidirectional entailment" in
      `docs/METHODOLOGY.md`.
- [ ] **Specifically removes the marked phenomenon**:
  - *Hyperbaton*: direct syntactic order (subject–verb–object), with no
    inversions that require reprocessing to figure out who does what to
    whom.
  - *Neologism*: replaced with current-vocabulary word(s) carrying the same
    intended sense — without inventing a new neologism to "translate" the
    old one.
  - *Metaphor*: literal sense made explicit; the simplification must not
    introduce a different metaphor in place of the original.
  - *Paradox*: the apparent logical tension is resolved/explained in direct
    language, without preserving the contradictory surface formulation.
- [ ] **Doesn't introduce new complexity**: the simplification shouldn't
      trade one complex phenomenon for another (e.g. resolving a hyperbaton
      but introducing a neologism in the chosen words).
- [ ] **Doesn't neutralize deliberate ambiguity that is part of the
      content**: if the original is genuinely ambiguous between two
      readings (and that ambiguity is part of what the text communicates,
      not an effect of the syntactic phenomenon itself), the simplification
      should preserve that ambiguity, not arbitrarily resolve it toward one
      side.
- [ ] **Neutral register**: register shifts (formal → colloquial, for
      example) are acceptable only to the extent required by the syntactic
      simplification; modernizing tone is not a goal of the exercise.

## Signs that a pair is problematic (shouldn't go in without review)

- The simplification adds an explanation/interpretation that isn't in the
  original (e.g. spelling out a cause, motivation, or judgment that the
  original leaves implicit or open).
- The simplification is short/long enough to suggest information was lost
  or added, not just reworded.
- The annotator can't articulate, in one sentence, why the two versions
  "say the same thing" — if the equivalence isn't defensible in plain
  prose, it's probably not a good intralingual translation.
- `nivel_confianca_equivalencia` below 4 without a note explaining the
  specific reservation in `notas`.

## Review process

1. `anotador_original` produces the pair and fills in
   `nivel_confianca_equivalencia` with their own honest assessment (don't
   inflate confidence).
2. A second annotator (`anotador_revisao`) evaluates the pair
   independently against the criteria above, without seeing the first
   annotator's confidence score before forming their own opinion.
3. Meaningful disagreements (e.g. a 2+ point difference in perceived
   confidence, or disagreement about either direction of entailment) are
   discussed and resolved before the pair enters `data/processed/`; the
   resolution (or the remaining disagreement) is recorded in `notas`.

## TODO (to refine during the pilot round)

- [ ] Calibrate concrete examples per author (Camões, Vieira, Gregório de
      Matos, Mário de Andrade, Pessoa/heteronyms) — what counts as "mild"
      vs. "pronounced" hyperbaton varies a lot between them.
- [ ] Define a minimum `nivel_confianca_equivalencia` threshold for a pair
      to be included in the "frozen" dataset used in the experiments (see
      TODO in `src/dataset/build_dataset.py`).
- [ ] Decide whether `fenomeno_linguistico` should stay a single category
      or move to multiple phenomena per fragment.
- [ ] Log annotated examples (good and problematic) in this document as the
      pilot round progresses.
