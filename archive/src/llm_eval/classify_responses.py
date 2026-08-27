"""Classifies LLM responses to detect hallucination / reasoning breakdown.

TODO: this module is not implemented yet — it's a stub for structure review
before writing the classification logic.

Planned responsibilities:
    - Read the raw responses persisted by `query_llms.py`.
    - Define and apply a taxonomy of interpretation failure induced by
      syntactic complexity, for example:
        * factual hallucination (asserts something not supported by the
          text);
        * logical reasoning breakdown (invalid inference from the text,
          even without inventing facts);
        * refusal/evasion (the model states it can't interpret the text);
        * correct interpretation.
      (Refine this taxonomy together with docs/ANNOTATION_GUIDE.md before
      implementing — decide whether classification will be human,
      automated via an LLM judge, or a hybrid protocol with sampling for
      inter-annotator agreement.)
    - Compare the failure rate between texto_original and
      texto_simplificado for the same fragment, by model and by
      fenomeno_linguistico, to test Phase 2's core hypothesis: the
      literary syntactic complexity of the original induces more
      interpretation failures than the intralingual translation of the
      same propositional content ("interpretive blindness").
    - Produce output tables/plots in results/.

See also:
    - src/llm_eval/query_llms.py
    - docs/METHODOLOGY.md, "Phase 2: Interpretive Blindness" section
"""

from __future__ import annotations

# TODO: implement. See module docstring for the planned scope.
