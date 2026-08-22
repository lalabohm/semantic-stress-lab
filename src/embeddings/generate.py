"""Gera embeddings para os pares (texto_original, texto_simplificado) do dataset.

TODO: este módulo ainda não está implementado — é um stub para revisão de
estrutura antes de escrever a lógica de chamada aos modelos.

Responsabilidades previstas:
    - Ler data/processed/dataset.jsonl (formato validado por
      src/dataset/schema.py::FragmentoDataset).
    - Para cada um dos modelos de embedding configurados — deliberadamente
      mais de um, para que os resultados da Fase 1 não dependam de uma
      única arquitetura de embedding —, gerar o vetor de `texto_original`
      e de `texto_simplificado`:
        * BGE-M3       (via sentence-transformers)
        * LaBSE        (via sentence-transformers)
        * EmbeddingGemma (via sentence-transformers, quando disponível)
    - Persistir os embeddings de forma reprodutível (ex. um .parquet ou
      .npz por modelo em results/, indexado por `id` do fragmento), para
      que `compare.py` não precise recalcular embeddings a cada execução.
    - Registrar metadados de proveniência (nome/versão do modelo, dimensão
      do vetor, timestamp) junto aos vetores.

Ver também:
    - src/embeddings/compare.py (cálculo de similaridade de cosseno a
      partir dos embeddings gerados aqui)
    - docs/METHODOLOGY.md, seção "Fase 1: Deriva Espacial nos Embeddings"
"""

from __future__ import annotations

# TODO: implementar. Ver docstring do módulo para o escopo previsto.
