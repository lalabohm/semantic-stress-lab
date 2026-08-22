"""Consolida múltiplos lotes de anotação em um único dataset validado.

TODO: este módulo ainda não está implementado — é um stub para revisão de
estrutura antes de escrever a lógica.

Responsabilidades previstas:
    - Descobrir e ler todos os .jsonl já convertidos em data/processed/
      (um por lote de anotação, gerado via `csv_to_jsonl.py`).
    - Detectar `id` duplicados entre lotes e decidir política de resolução
      (erro? manter o mais recente? exigir anotador_revisao preenchido?).
    - Aplicar filtros de qualidade agregados, ex.:
        * descartar (ou sinalizar) registros com
          `nivel_confianca_equivalencia` abaixo de um limiar configurável;
        * exigir `anotador_revisao` preenchido antes de entrar no dataset
          "final" usado nos experimentos (distinguir dataset em revisão vs.
          dataset congelado para a Fase 1/Fase 2).
    - Escrever o dataset consolidado final (ex. data/processed/dataset.jsonl)
      e, possivelmente, um relatório de cobertura por autor/fenômeno
      linguístico para orientar quais lacunas ainda precisam de anotação.

Ver também:
    - src/dataset/schema.py       (schema canônico / validação por registro)
    - src/dataset/csv_to_jsonl.py (conversão de um lote CSV -> JSONL)
    - docs/ANNOTATION_GUIDE.md    (critérios de qualidade da anotação)
"""

from __future__ import annotations

# TODO: implementar. Ver docstring do módulo para o escopo previsto.
