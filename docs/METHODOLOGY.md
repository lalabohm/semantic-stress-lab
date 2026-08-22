# Metodologia

## Hipótese central

Complexidade sintático-literária — hipérbato, neologismo, metáfora, paradoxo —
degrada a fidelidade semântica de embeddings e induz falhas de raciocínio em
LLMs durante tarefas de interpretação, mesmo quando o conteúdo proposicional
do texto é preservado. Testamos isso comparando cada fragmento literário
original a uma "tradução intralingual" — uma reescrita em português
contemporâneo, sintaticamente direta, que remove o fenômeno estudado sem
alterar o que é dito.

Se a hipótese for correta, o par (original, simplificado) deve se comportar
de forma assimetricamente pior para o original em duas frentes independentes:
geometria de embeddings (Fase 1) e interpretação por LLMs (Fase 2).

## Protocolo de tradução intralingual

A "tradução intralingual" é o par produzido para cada fragmento original e é
o insumo mais sensível do experimento: se ela não for de fato equivalente em
conteúdo proposicional, qualquer diferença medida na Fase 1/Fase 2 pode
refletir divergência de conteúdo, não a complexidade sintática em si. O
protocolo, portanto, prioriza a equivalência semântica acima de fluência ou
elegância.

**Objetivo da reescrita**: preservar o que o texto afirma, pergunta, nega ou
implica logicamente, enquanto se remove o fenômeno linguístico marcado
(`fenomeno_linguistico`) — reordenando sintaxe hiperbática para ordem direta
SVO, substituindo neologismos por paráfrase em vocabulário corrente,
explicitando o sentido literal por trás da metáfora, resolvendo a tensão
aparente do paradoxo em linguagem direta.

**Checagem de equivalência — entailment bidirecional**: antes de um par
entrar no dataset final, o anotador (e, na revisão, um segundo anotador)
deve poder afirmar as duas direções de implicação lógica:

1. `texto_original` implica `texto_simplificado` — nada foi acrescentado na
   simplificação que não estivesse (ainda que implicitamente) no original.
2. `texto_simplificado` implica `texto_original` — nada do conteúdo do
   original foi perdido ou enfraquecido na simplificação.

Quando o anotador não consegue sustentar as duas direções com confiança, o
par não é "boa tradução intralingual" — ver critérios detalhados em
`docs/ANNOTATION_GUIDE.md`. O campo `nivel_confianca_equivalencia`
(escala 1–5) registra o grau de confiança nessa checagem bidirecional, e
`anotador_revisao` registra quem forneceu a segunda opinião.

Este protocolo é deliberadamente humano nesta fase do projeto. Uma checagem
automática de entailment (ex. via um modelo de NLI ou um LLM-juiz) é uma
extensão possível para validar em escala os pares já anotados, mas não
substitui a anotação humana como critério de inclusão no dataset.

## Fase 1: Deriva Espacial nos Embeddings

**Pergunta**: fragmentos com maior complexidade sintático-literária produzem
uma similaridade de cosseno menor entre `texto_original` e
`texto_simplificado` do que fragmentos sintaticamente diretos — mesmo quando
ambos os membros do par são, por construção, semanticamente equivalentes?

**Desenho**:
1. Gerar embeddings de `texto_original` e `texto_simplificado` para cada par,
   usando múltiplos modelos de embedding (BGE-M3, LaBSE, EmbeddingGemma), de
   modo que a conclusão não dependa de uma arquitetura específica.
2. Calcular a similaridade de cosseno entre os dois vetores de cada par, por
   modelo.
3. Agregar a similaridade por `fenomeno_linguistico` e por autor, e comparar
   as distribuições entre fenômenos e entre modelos.

**Leitura esperada sob a hipótese**: pares cujo original é marcado com
hipérbato acentuado, neologismo denso ou metáfora opaca devem apresentar
similaridade de cosseno sistematicamente menor do que pares cujo original já
é sintaticamente próximo da "tradução" (efeito de "deriva espacial" do
fragmento complexo em relação ao seu conteúdo proposicional real, medido no
espaço de embedding).

Ver stubs de implementação em `src/embeddings/generate.py` e
`src/embeddings/compare.py`.

## Fase 2: Cegueira Interpretativa

**Pergunta**: LLMs cometem mais erros de interpretação/inferência lógica —
alucinação, quebra de raciocínio, recusa — ao processar `texto_original` do
que ao processar `texto_simplificado` do mesmo par, e essa diferença escala
com a complexidade sintático-literária do fragmento?

**Desenho**:
1. Submeter `texto_original` e `texto_simplificado` de cada par,
   separadamente, a múltiplos LLMs (Gemini 2.5 Flash, Qwen3 via Ollama
   local, Llama 3.3 via Groq), com um prompt padronizado de
   interpretação/inferência lógica.
2. Classificar cada resposta segundo uma taxonomia de falha (alucinação
   factual, quebra de raciocínio, recusa/evasão, interpretação correta —
   taxonomia a refinar, ver `docs/ANNOTATION_GUIDE.md` e o stub de
   `src/llm_eval/classify_responses.py`).
3. Comparar a taxa de falha entre `texto_original` e `texto_simplificado`
   para o mesmo fragmento, por modelo e por `fenomeno_linguistico`.

**Leitura esperada sob a hipótese**: a taxa de falha de interpretação é
maior para `texto_original` do que para `texto_simplificado` do mesmo par, e
essa diferença ("cegueira interpretativa") é mais pronunciada nos fenômenos
linguísticos de maior complexidade sintática.

Ver stubs de implementação em `src/llm_eval/query_llms.py` e
`src/llm_eval/classify_responses.py`.

## Status

Fase de construção do dataset. As Fases 1 e 2 dependem de um dataset
validado em `data/processed/dataset.jsonl`; a lógica de chamada a
embeddings/LLMs ainda não foi implementada (apenas stubs com TODOs).
