"""Sanity tests for the dataset schema (src/dataset/schema.py).

These cover only the structural/type validation of FragmentoDataset.
Linguistic content tests (e.g. intralingual translation quality) belong to
the human review described in docs/ANNOTATION_GUIDE.md, not to this file.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.dataset.schema import FenomenoLinguistico, FragmentoDataset

VALID_RECORD = {
    "id": "camoes-lusiadas-001",
    "autor": "Luís de Camões",
    "obra": "Os Lusíadas",
    "ano_publicacao": 1572,
    "fenomeno_linguistico": "hiperbato",
    "texto_original": "As armas e os barões assinalados...",
    "texto_simplificado": "Os soldados e os homens ilustres, com as armas...",
    "anotador_original": "lalabohm",
    "anotador_revisao": None,
    "nivel_confianca_equivalencia": 4,
    "notas": None,
}


def test_valid_record_parses():
    record = FragmentoDataset(**VALID_RECORD)
    assert record.fenomeno_linguistico is FenomenoLinguistico.HIPERBATO


def test_missing_required_field_raises():
    incomplete = dict(VALID_RECORD)
    del incomplete["texto_original"]
    with pytest.raises(ValidationError):
        FragmentoDataset(**incomplete)


def test_invalid_fenomeno_raises():
    invalid = dict(VALID_RECORD, fenomeno_linguistico="anacoluto")
    with pytest.raises(ValidationError):
        FragmentoDataset(**invalid)


def test_confianca_out_of_scale_raises():
    invalid = dict(VALID_RECORD, nivel_confianca_equivalencia=6)
    with pytest.raises(ValidationError):
        FragmentoDataset(**invalid)


def test_blank_text_raises():
    invalid = dict(VALID_RECORD, texto_simplificado="   ")
    with pytest.raises(ValidationError):
        FragmentoDataset(**invalid)


def test_optional_fields_default_to_none():
    minimal = dict(VALID_RECORD)
    del minimal["ano_publicacao"]
    del minimal["anotador_revisao"]
    del minimal["notas"]
    record = FragmentoDataset(**minimal)
    assert record.ano_publicacao is None
    assert record.anotador_revisao is None
    assert record.notas is None
