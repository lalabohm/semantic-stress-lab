"""Classifica respostas de LLMs para detectar alucinação / quebra de raciocínio.

TODO: este módulo ainda não está implementado — é um stub para revisão de
estrutura antes de escrever a lógica de classificação.

Responsabilidades previstas:
    - Ler as respostas cruas persistidas por `query_llms.py`.
    - Definir e aplicar uma taxonomia de falha de interpretação induzida
      pela complexidade sintática, por exemplo:
        * alucinação factual (afirma algo não sustentado pelo texto);
        * quebra de raciocínio lógico (inferência inválida a partir do
          texto, mesmo sem inventar fatos);
        * recusa/evasão (o modelo declara não conseguir interpretar);
        * interpretação correta.
      (Refinar esta taxonomia junto com docs/ANNOTATION_GUIDE.md antes de
      implementar — decidir se a classificação será humana, automática via
      um LLM-juiz, ou um protocolo híbrido com amostragem para acordo
      inter-anotador.)
    - Comparar a taxa de falha entre texto_original e texto_simplificado
      para o mesmo fragmento, por modelo e por fenomeno_linguistico, para
      testar a hipótese central da Fase 2: a complexidade sintático-
      literária do original induz mais falhas de interpretação do que a
      tradução intralingual do mesmo conteúdo proposicional
      ("cegueira interpretativa").
    - Produzir tabelas/gráficos de saída em results/.

Ver também:
    - src/llm_eval/query_llms.py
    - docs/METHODOLOGY.md, seção "Fase 2: Cegueira Interpretativa"
"""

from __future__ import annotations

# TODO: implementar. Ver docstring do módulo para o escopo previsto.
