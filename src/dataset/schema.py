"""Schema canônico do dataset do Laboratório de Estresse Semântico.

Cada registro do dataset representa um par (fragmento original / fragmento
"traduzido intralingualmente") anotado por um humano, junto com metadados
bibliográficos e de controle de qualidade da anotação.

Este módulo é a fonte única de verdade sobre o formato dos dados: tanto o
conversor CSV -> JSONL (`csv_to_jsonl.py`) quanto qualquer código downstream
(geração de embeddings, avaliação de LLMs) devem validar contra o modelo
`FragmentoDataset` definido aqui, em vez de reimplementar as regras.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FenomenoLinguistico(str, Enum):
    """Fenômeno sintático-literário predominante no fragmento original.

    Se um fragmento exibir mais de um fenômeno de forma proeminente, o
    anotador deve escolher o dominante para efeitos de agrupamento estatístico
    e registrar os demais em `notas`. (Revisar esta decisão de design ao
    longo da fase de anotação piloto — pode fazer sentido migrar para uma
    lista de fenômenos por fragmento.)
    """

    HIPERBATO = "hiperbato"
    NEOLOGISMO = "neologismo"
    METAFORA = "metafora"
    PARADOXO = "paradoxo"


class FragmentoDataset(BaseModel):
    """Um par (original, tradução intralingual) com metadados de anotação.

    `texto_original` é o fragmento extraído verbatim da obra em domínio
    público. `texto_simplificado` é a reescrita produzida seguindo o
    protocolo de tradução intralingual descrito em
    `docs/METHODOLOGY.md` (equivalência semântica + entailment
    bidirecional), cujo objetivo é remover o fenômeno sintático-literário
    marcado em `fenomeno_linguistico` sem alterar o conteúdo proposicional.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(..., min_length=1, description="Identificador único do par, ex. 'camoes-lusiadas-001'.")
    autor: str = Field(..., min_length=1, description="Nome do autor, ex. 'Luís de Camões'.")
    obra: str = Field(..., min_length=1, description="Obra de origem, ex. 'Os Lusíadas'.")
    ano_publicacao: Optional[int] = Field(
        default=None,
        gt=0,
        description="Ano de publicação da obra (ou de composição, se anterior à publicação).",
    )
    fenomeno_linguistico: FenomenoLinguistico = Field(
        ..., description="Fenômeno sintático-literário predominante sendo testado."
    )
    texto_original: str = Field(..., min_length=1, description="Fragmento original, verbatim.")
    texto_simplificado: str = Field(
        ..., min_length=1, description="Tradução intralingual (versão simplificada) do fragmento."
    )
    anotador_original: str = Field(..., min_length=1, description="Identificação de quem produziu a tradução intralingual.")
    anotador_revisao: Optional[str] = Field(
        default=None, description="Identificação de quem revisou o par (segunda opinião), se houver."
    )
    nivel_confianca_equivalencia: int = Field(
        ...,
        ge=1,
        le=5,
        description=(
            "Escala Likert (1-5) de confiança do(s) anotador(es) de que "
            "texto_original e texto_simplificado são semanticamente "
            "equivalentes (ver critérios em docs/ANNOTATION_GUIDE.md)."
        ),
    )
    notas: Optional[str] = Field(default=None, description="Observações livres do anotador ou revisor.")

    @field_validator("texto_original", "texto_simplificado")
    @classmethod
    def _texto_nao_vazio_apos_strip(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("texto não pode ser vazio ou conter apenas espaços em branco")
        return v
