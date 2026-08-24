"""Canonical dataset schema for the Semantic Stress Lab.

Each dataset record represents a (original fragment / "intralingually
translated" fragment) pair annotated by a human, along with bibliographic
metadata and annotation quality-control fields.

This module is the single source of truth for the data format: both the
CSV -> JSONL converter (`csv_to_jsonl.py`) and any downstream code
(embedding generation, LLM evaluation) should validate against the
`DatasetEntry` model defined here, instead of reimplementing the rules.

Field names are kept in Portuguese, matching the Portuguese-language
literary corpus and annotation workflow the dataset describes.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

NIVEIS_CONFIANCA_VALIDOS = {"alta", "média", "baixa"}


class DatasetEntry(BaseModel):
    """An (original, intralingual translation) pair with annotation metadata.

    `texto_original` is the fragment extracted verbatim from the
    public-domain work. `texto_simplificado` is the rewrite produced
    following the intralingual translation protocol, whose goal is to
    remove the literary phenomenon marked in `fenomeno_linguistico`
    without changing the propositional content.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(..., min_length=1, description="Unique identifier for the pair, e.g. 'vieira_001'.")
    autor: str = Field(..., min_length=1, description="Author name, e.g. 'Padre Antônio Vieira'.")
    obra: str = Field(..., min_length=1, description="Source work, e.g. 'Sermão da Sexagésima'.")
    ano_publicacao: int = Field(..., gt=0, description="Publication year of the work.")
    fenomeno_linguistico: str = Field(
        ..., min_length=1, description="Dominant literary phenomenon being tested."
    )
    texto_original: str = Field(..., min_length=1, description="Original fragment, verbatim.")
    texto_simplificado: str = Field(
        ..., min_length=1, description="Intralingual translation (simplified version) of the fragment."
    )
    anotador_original: str = Field(..., min_length=1, description="Identifier of who produced the intralingual translation.")
    anotador_revisao: Optional[str] = Field(
        default=None, description="Identifier of who reviewed the pair (second opinion), if any."
    )
    nivel_confianca_equivalencia: str = Field(
        ...,
        description=(
            "Annotator(s)' confidence that texto_original and "
            "texto_simplificado are semantically equivalent. "
            f"Must be one of: {sorted(NIVEIS_CONFIANCA_VALIDOS)}."
        ),
    )
    notas: str = Field(default="", description="Free-form notes from the annotator or reviewer. May be empty.")

    @field_validator("texto_original", "texto_simplificado")
    @classmethod
    def _text_not_blank_after_strip(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty or contain only whitespace")
        return v

    @field_validator("nivel_confianca_equivalencia")
    @classmethod
    def _nivel_confianca_valido(cls, v: str) -> str:
        if v not in NIVEIS_CONFIANCA_VALIDOS:
            raise ValueError(
                f"must be one of {sorted(NIVEIS_CONFIANCA_VALIDOS)}, got {v!r}"
            )
        return v
