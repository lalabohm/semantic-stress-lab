# Laboratório de Estresse Semântico

Pesquisa adversarial sobre como a complexidade sintático-literária —
hipérbato, neologismo, metáfora, paradoxo — degrada a fidelidade de
embeddings e induz alucinação/quebra de raciocínio em LLMs durante tarefas
de interpretação (RAG), usando pares de fragmentos literários em português
em domínio público (Camões, Padre Antônio Vieira, Gregório de Matos, Mário
de Andrade, Fernando Pessoa e heterônimos) contra sua "tradução
intralingual" (versão simplificada, semanticamente equivalente).

O experimento tem duas fases:

- **Fase 1 — Deriva Espacial nos Embeddings**: compara a similaridade de
  cosseno entre original e simplificado usando múltiplos modelos de
  embedding (BGE-M3, LaBSE, EmbeddingGemma), para não depender de uma única
  arquitetura.
- **Fase 2 — Cegueira Interpretativa**: submete original e simplificado a
  múltiplos LLMs (Gemini 2.5 Flash, Qwen3 via Ollama local, Llama 3.3 via
  Groq) e classifica as respostas para detectar alucinação ou quebra de
  raciocínio induzida pela complexidade sintática.

Metodologia completa, incluindo o protocolo de tradução intralingual e a
checagem de entailment bidirecional, em [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).
Critérios de anotação em [`docs/ANNOTATION_GUIDE.md`](docs/ANNOTATION_GUIDE.md).

## Status atual

🚧 Fase de construção do dataset. O schema (`src/dataset/schema.py`) e o
conversor CSV → JSONL (`src/dataset/csv_to_jsonl.py`) estão implementados e
testados. A lógica de geração de embeddings e de chamada aos LLMs
(`src/embeddings/`, `src/llm_eval/`) ainda são stubs — Fases 1 e 2 ainda não
foram executadas.

## Estrutura de pastas

```
data/
  raw/            textos originais extraídos, organizados por autor
  processed/      dataset final consolidado, em .jsonl
  annotation/     planilhas/CSVs de trabalho para revisão humana
src/
  dataset/        construção e validação do dataset (schema, CSV -> JSONL)
  embeddings/     geração e comparação de embeddings (Fase 1) — stub
  llm_eval/       chamada aos LLMs e classificação de respostas (Fase 2) — stub
notebooks/        análise exploratória
docs/             METHODOLOGY.md, ANNOTATION_GUIDE.md
results/          outputs de experimentos, gráficos, tabelas
tests/            testes automatizados
```

## Setup do ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure as chaves de API necessárias para a Fase 2:

```bash
cp .env.example .env
# edite .env com GOOGLE_API_KEY e GROQ_API_KEY
```

Qwen3 roda localmente via [Ollama](https://ollama.com/) — não requer chave,
mas requer o serviço rodando (`ollama serve`) e o modelo baixado
(`ollama pull qwen3`).

## Como rodar

**Construir o dataset** a partir de uma planilha de anotação:

```bash
python -m src.dataset.csv_to_jsonl \
  --input data/annotation/lote_01.csv \
  --output data/processed/dataset.jsonl
```

Veja `data/annotation/exemplo.csv` para o formato de colunas esperado (um
por campo de `FragmentoDataset` em `src/dataset/schema.py`).

**Rodar os testes**:

```bash
pytest
```

**Gerar embeddings** (Fase 1) e **rodar avaliação de LLMs** (Fase 2): ainda
não implementado — ver TODOs em `src/embeddings/generate.py`,
`src/embeddings/compare.py`, `src/llm_eval/query_llms.py` e
`src/llm_eval/classify_responses.py`.
