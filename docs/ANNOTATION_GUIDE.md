# Guia de Anotação

> Esqueleto inicial — critérios a refinar durante a rodada piloto de
> anotação. Ver `docs/METHODOLOGY.md` para o protocolo de tradução
> intralingual e a checagem de entailment bidirecional que este guia
> operacionaliza.

## O que o anotador está produzindo

Para cada fragmento original selecionado (`texto_original`), o anotador
escreve uma **tradução intralingual** (`texto_simplificado`): uma reescrita
em português contemporâneo que remove o `fenomeno_linguistico` marcado
(hipérbato, neologismo, metáfora ou paradoxo) preservando o conteúdo
proposicional do original — o que ele afirma, nega, pergunta ou implica.

O objetivo **não** é produzir uma paráfrase elegante ou uma "modernização
literária". É produzir o texto mais direto e sintaticamente neutro possível
que ainda diz exatamente a mesma coisa que o original.

## Critérios de uma boa tradução intralingual

- [ ] **Equivalência proposicional bidirecional**: o original implica a
      simplificação e a simplificação implica o original (nenhum conteúdo
      foi acrescentado nem perdido). Ver "entailment bidirecional" em
      `docs/METHODOLOGY.md`.
- [ ] **Remove especificamente o fenômeno marcado**:
  - *Hipérbato*: ordem sintática direta (sujeito–verbo–objeto), sem
    inversões que exijam reprocessamento para entender quem faz o quê a quem.
  - *Neologismo*: substituído por palavra(s) de vocabulário corrente com o
    mesmo sentido pretendido — sem inventar um neologismo novo para "traduzir"
    o antigo.
  - *Metáfora*: sentido literal explicitado; a simplificação não deve
    introduzir uma metáfora diferente para substituir a original.
  - *Paradoxo*: a tensão lógica aparente é resolvida/explicada em linguagem
    direta, sem preservar a formulação contraditória de superfície.
- [ ] **Não introduz complexidade nova**: a simplificação não deve trocar um
      fenômeno complexo por outro (ex. resolver um hipérbato mas introduzir
      um neologismo nas palavras escolhidas).
- [ ] **Não neutraliza ambiguidade proposital que faz parte do conteúdo**:
      se o original é genuinamente ambíguo entre duas leituras (e isso é
      parte do que o texto comunica, não um efeito do fenômeno sintático em
      si), a simplificação deve preservar essa ambiguidade, não resolvê-la
      arbitrariamente para um dos lados.
- [ ] **Registro neutro**: mudanças de registro (formal → coloquial, por
      exemplo) são aceitáveis apenas na medida em que forem necessárias para
      a simplificação sintática; não é objetivo do exercício modernizar o
      tom.

## Sinais de que um par é problemático (não deve entrar sem revisão)

- A simplificação acrescenta uma explicação/interpretação que não está no
  original (ex. explicitar uma causa, motivação ou avaliação que o original
  deixa implícita ou em aberto).
- A simplificação é mais curta/longa a ponto de sugerir que informação foi
  perdida ou adicionada, e não apenas reformulada.
- O anotador não consegue articular, em uma frase, por que as duas versões
  "dizem a mesma coisa" — se a equivalência não é defensável em prosa
  simples, provavelmente não é uma boa tradução intralingual.
- `nivel_confianca_equivalencia` abaixo de 4 sem uma nota explicando a
  reserva específica em `notas`.

## Processo de revisão

1. `anotador_original` produz o par e preenche `nivel_confianca_equivalencia`
   com sua própria avaliação honesta (não infle a confiança).
2. Um segundo anotador (`anotador_revisao`) avalia o par de forma
   independente contra os critérios acima, sem ver a nota de confiança do
   primeiro anotador antes de formar sua própria opinião.
3. Divergências relevantes (ex. diferença de 2+ pontos na confiança
   percebida, ou discordância sobre alguma das direções do entailment) são
   discutidas e resolvidas antes do par entrar em `data/processed/`; a
   resolução (ou a divergência remanescente) é registrada em `notas`.

## TODO (a refinar na rodada piloto)

- [ ] Calibrar exemplos concretos por autor (Camões, Vieira, Gregório de
      Matos, Mário de Andrade, Pessoa/heterônimos) — o que conta como
      hipérbato "leve" vs. "acentuado" varia muito entre eles.
- [ ] Definir um limiar mínimo de `nivel_confianca_equivalencia` para um par
      ser incluído no dataset "congelado" usado nos experimentos (ver TODO
      em `src/dataset/build_dataset.py`).
- [ ] Decidir se `fenomeno_linguistico` deve permanecer categórico único ou
      migrar para múltiplos fenômenos por fragmento.
- [ ] Registrar exemplos anotados (bons e problemáticos) neste documento
      conforme a rodada piloto avançar.
