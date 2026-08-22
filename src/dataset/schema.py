"""Canonical dataset schema for the Semantic Stress Lab.

Each dataset record represents a (original fragment / "intralingually
translated" fragment) pair annotated by a human, along with bibliographic
metadata and annotation quality-control fields.

This module is the single source of truth for the data format: both the
CSV -> JSONL converter (`csv_to_jsonl.py`) and any downstream code
(embedding generation, LLM evaluation) should validate against the
`FragmentoDataset` model defined here, instead of reimplementing the rules.

Field names and enum values are kept in Portuguese, matching the
Portuguese-language literary corpus and annotation workflow the dataset
describes.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FenomenoLinguistico(str, Enum):
    """Dominant literary syntactic phenomenon in the original fragment.

    If a fragment prominently exhibits more than one phenomenon, the
    annotator should pick the dominant one for statistical grouping
    purposes and record the others in `notas`. (Revisit this design
    decision during the pilot annotation phase — it may make sense to
    move to a list of phenomena per fragment.)
    """

    HIPERBATO = "hiperbato"
    NEOLOGISMO = "neologismo"
    METAFORA = "metafora"
    PARADOXO = "paradoxo"


class FragmentoDataset(BaseModel):
    """An (original, intralingual translation) pair with annotation metadata.

    `texto_original` is the fragment extracted verbatim from the
    public-domain work. `texto_simplificado` is the rewrite produced
    following the intralingual translation protocol described in
    `docs/METHODOLOGY.md` (semantic equivalence + bidirectional
    entailment), whose goal is to remove the literary syntactic phenomenon
    marked in `fenomeno_linguistico` without changing the propositional
    content.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(..., min_length=1, description="Unique identifier for the pair, e.g. 'camoes-lusiadas-001'.")
    autor: str = Field(..., min_length=1, description="Author name, e.g. 'Luís de Camões'.")
    obra: str = Field(..., min_length=1, description="Source work, e.g. 'Os Lusíadas'.")
    ano_publicacao: Optional[int] = Field(
        default=None,
        gt=0,
        description="Publication year of the work (or composition year, if earlier than publication).",
    )
    fenomeno_linguistico: FenomenoLinguistico = Field(
        ..., description="Dominant literary syntactic phenomenon being tested."
    )
    texto_original: str = Field(..., min_length=1, description="Original fragment, verbatim.")
    texto_simplificado: str = Field(
        ..., min_length=1, description="Intralingual translation (simplified version) of the fragment."
    )
    anotador_original: str = Field(..., min_length=1, description="Identifier of who produced the intralingual translation.")
    anotador_revisao: Optional[str] = Field(
        default=None, description="Identifier of who reviewed the pair (second opinion), if any."
    )
    nivel_confianca_equivalencia: int = Field(
        ...,
        ge=1,
        le=5,
        description=(
            "Likert scale (1-5) of the annotator(s)' confidence that "
            "texto_original and texto_simplificado are semantically "
            "equivalent (see criteria in docs/ANNOTATION_GUIDE.md)."
        ),
    )
    notas: Optional[str] = Field(default=None, description="Free-form notes from the annotator or reviewer.")

    @field_validator("texto_original", "texto_simplificado")
    @classmethod
    def _text_not_blank_after_strip(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty or contain only whitespace")
        return v
