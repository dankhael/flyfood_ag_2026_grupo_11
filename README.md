# FlyFood AG 2026 — Brasil58 (TSP com Algoritmo Genético)

Resolução do problema do **Caixeiro Viajante (TSP)** sobre a instância **Brasil58** (58 cidades brasileiras) usando um **Algoritmo Genético (AG)** com seleção de sobreviventes **steady-state**.

> **TL;DR — quero só rodar:**
> ```bash
> python algoritmoGeneticoBrasil58.py
> ```
> Veja a seção [5. Como executar](#5-como-executar) para detalhes.

---

## 1. O problema do Caixeiro Viajante (TSP)

Dado um conjunto de cidades e as distâncias entre cada par delas, o objetivo é encontrar a **rota de menor custo** que:

- Passa por **todas** as cidades exatamente uma vez;
- Retorna à cidade de origem ao final.

Matematicamente é um problema **NP-difícil**: o número de rotas possíveis cresce com `(n-1)!/2`. Para 58 cidades isso dá cerca de 10⁷⁶ rotas — impossível testar todas por força bruta. Por isso usamos uma **meta-heurística** como o AG: ela **não garante** o ótimo, mas encontra boas soluções em tempo razoável.

### A instância Brasil58

- 58 cidades brasileiras;
- Distâncias armazenadas em formato de **matriz triangular superior** no arquivo `edgesbrasil58.tsp`;
- Ótimo conhecido: **25395** (referência para avaliar a qualidade da nossa solução).

---

## 2. Como um Algoritmo Genético funciona (a ideia geral)

Um AG imita a **evolução natural**. Trabalhamos com uma **população** de soluções candidatas e, a cada **geração**, fazemos os melhores "se reproduzirem" e os piores "morrerem". Com o tempo, a população evolui para soluções cada vez melhores.

O ciclo básico é:

```
1. Crie uma população inicial aleatória
2. Avalie a qualidade (aptidão) de cada indivíduo
3. Repita por várias gerações:
     a. SELEÇÃO DE PAIS    → escolhe quem se reproduz
     b. CROSSOVER          → combina dois pais e gera filhos
     c. MUTAÇÃO            → introduz pequenas variações aleatórias
     d. SELEÇÃO DE          → decide quem sobrevive para a próxima geração
        SOBREVIVENTES
4. Devolve o melhor indivíduo já encontrado
```

Cada uma dessas etapas é detalhada na seção 4.

---

## 3. Estrutura do projeto

| Arquivo | Função |
|---|---|
| `edgesbrasil58.tsp` | Dados das distâncias entre as cidades (matriz triangular superior) |
| `lerBrasil58.py` | Lê o arquivo, monta o dicionário de distâncias e define as funções de custo e de inicialização da população |
| `algoritmoGeneticoBrasil58.py` | Loop principal do AG: seleção, crossover, mutação e seleção de sobreviventes |
| `conversorMatrizParaDistancias.py` | Converte uma matriz de pontos (R, A, B, …) em arquivo de distâncias |
| `exemplo_entrada.txt` | Exemplo de matriz de pontos para o conversor |
| `brazil58.tsp` | Arquivo original da instância Brasil58 (formato completo) |
| `tests/` | Testes automatizados (pytest) — ver seção 8 |
| `conftest.py`, `pytest.ini` | Configuração e ajudantes compartilhados dos testes |

---

## 4. Como o código funciona (passo a passo)

### 4.1 Representação do indivíduo

Cada **indivíduo** (uma rota candidata) é uma **permutação** das cidades 1 a 58:

```python
individuo = [5, 14, 2, 3, 7, ...]   # visita 5, depois 14, depois 2...
```

A **população** é simplesmente uma lista de indivíduos.

### 4.2 Função de aptidão (fitness)

A função `custoCaminho` (em `lerBrasil58.py`) soma as distâncias entre cidades consecutivas e adiciona o retorno à origem:

```
custo = d(p0, p1) + d(p1, p2) + ... + d(pn-1, pn) + d(pn, p0)
```

Como queremos **minimizar** o custo, **quanto menor o custo, melhor o indivíduo**.

### 4.3 Seleção de pais — Torneio (k=5)

Para cada filho a ser gerado, sorteamos `k` indivíduos da população e o de **menor custo vence** o torneio, tornando-se um dos pais. Vantagens:

- Não exige normalizar a aptidão (ideal para problemas de minimização);
- A "pressão seletiva" é ajustada por `k`: um `k` maior favorece os melhores; um `k` menor preserva mais diversidade.

### 4.4 Crossover — Order Crossover (OX1)

Um crossover comum quebraria a permutação (geraria rotas com cidades repetidas ou ausentes). O **OX1** preserva a propriedade de permutação:

1. Sorteia um trecho `[a..b]` no pai1 e o copia para o filho;
2. Percorre o pai2 a partir de `b+1` (de forma circular) e preenche as posições restantes do filho **na ordem em que as cidades aparecem no pai2**, ignorando as que já vieram no trecho copiado.

Resultado: o filho herda uma **subsequência contígua** do pai1 e a **ordem relativa** das demais cidades do pai2.

### 4.5 Mutações

Duas mutações com taxas independentes:

**Inversion** — inverte um trecho aleatório:
```
[1 2 3 4 5 6 7]  →  [1 2 6 5 4 3 7]
```
É a base do clássico **2-opt** em TSP. Preserva quase todas as arestas adjacentes, alterando apenas duas — uma modificação local e muito eficaz.

**Scramble** — embaralha um trecho aleatório:
```
[1 2 3 4 5 6 7]  →  [1 2 5 3 6 4 7]
```
Mais disruptiva. Ajuda a **escapar de ótimos locais** quando a população começa a convergir cedo demais.

### 4.6 Seleção de sobreviventes — Steady-state (μ + λ)

Esta é a etapa que decide **quem passa para a próxima geração**. Existem duas abordagens clássicas:

- **Geracional** (❌ evitamos): os filhos **substituem totalmente** a população anterior. Risco: um bom pai pode ser perdido se os filhos saírem piores.
- **Steady-state** (✅ usamos): juntamos **pais + filhos** num único conjunto e selecionamos os **melhores** dele para formar a próxima população.

A função `selecaoSobreviventes` faz exatamente isso, com uma proteção extra contra **convergência prematura**:

```
conjunto = pais + filhos          # mescla os dois grupos
ordena por custo (menor primeiro)
separa indivíduos ÚNICOS das duplicatas (rotas idênticas)
sobreviventes = os melhores ÚNICOS;
                duplicatas só entram para completar a população
```

Vantagem fundamental: como sempre escolhemos os melhores do conjunto combinado, **o melhor indivíduo nunca é perdido** (elitismo *implícito*). Não é preciso uma etapa separada de elitismo — ela já está embutida na seleção.

**Por que eliminar duplicatas?** O steady-state elitista tende a encher a população de **cópias do melhor indivíduo**. Quando isso acontece, o crossover combina pais idênticos e gera filhos idênticos, e a busca **estagna num ótimo local** logo nas primeiras gerações. Ao priorizar rotas *únicas*, mantemos a diversidade viva: a busca continua produtiva por muito mais gerações e chega bem mais perto do ótimo. Na prática, essa única mudança reduziu o *gap* para o ótimo de ~2,3% para ~0,5%.

### 4.7 Loop principal (com steady-state)

```
inicializa população aleatória (pais)
calcula a aptidão dos pais
repete por NUM_GERACOES:
    filhos = []
    enquanto não houver NUM_FILHOS filhos:
        pai1 = torneio(k=5)
        pai2 = torneio(k=5)
        filho1, filho2 = orderCrossover(pai1, pai2)   # com prob. TAXA_CROSSOVER
        aplica mutações nos filhos
        adiciona filhos à lista
    calcula a aptidão dos filhos
    população = selecaoSobreviventes(pais + filhos)   # STEADY-STATE
    atualiza o melhor global
devolve o melhor indivíduo encontrado
```

---

## 5. Como executar

**Pré-requisito:** Python 3 instalado. O projeto usa apenas a biblioteca padrão — **não há dependências para instalar**.

Rode o AG sobre a instância Brasil58:

```bash
python algoritmoGeneticoBrasil58.py
```

O que acontece:

- A cada 50 gerações o programa imprime o **melhor custo da geração** e o **melhor custo global**;
- Ao final, imprime a **rota encontrada** e o seu **custo**.

Compare o custo final com o ótimo conhecido (**25395**) para avaliar quão boa foi a solução. Quanto mais perto, melhor.

> **Reprodutibilidade:** por padrão o `random.seed()` usa uma semente aleatória, então cada execução dá um resultado diferente. Para repetir exatamente o mesmo resultado, fixe a semente em `algoritmoGeneticoBrasil58.py` (ex.: `random.seed(42)`).

---

## 6. Parâmetros configuráveis

No topo de `algoritmoGeneticoBrasil58.py`:

| Parâmetro | Valor padrão | Efeito |
|---|---|---|
| `TAMANHO_POPULACAO` | 200 | Maior = mais diversidade, porém mais lento |
| `NUM_GERACOES` | 16000 | Critério de parada (quantas gerações rodar) |
| `TAXA_CROSSOVER` | 0.9 | Probabilidade de aplicar o OX1 |
| `TAXA_MUT_INVERSAO` | 0.5 | Probabilidade de inverter um trecho |
| `TAXA_MUT_SCRAMBLE` | 0.10 | Probabilidade de embaralhar um trecho |
| `TAMANHO_TORNEIO` | 5 | Pressão seletiva na escolha dos pais |
| `NUM_FILHOS` | 50 | Quantos filhos gerar por geração (o λ do steady-state) |

Estes valores foram escolhidos por experimentação (busca em grade com várias sementes). As principais lições:

- **`NUM_FILHOS` < `TAMANHO_POPULACAO`** (λ pequeno): cada geração é mais barata, então cabem muito mais gerações de **refinamento** no mesmo tempo — a essência do steady-state.
- **Taxa de inversão alta (0.5)** acelera a melhoria local (a inversion é a base do 2-opt).
- **Pressão seletiva moderada (k=5)** equilibra convergência e diversidade.

Com esses ajustes (mais a eliminação de duplicatas da seção 4.6), o resultado típico fica em torno de **0,5% acima do ótimo** (frequentemente atingindo o próprio ótimo, 25395), e ainda **mais rápido** que a configuração inicial.

Dica: aumentar `NUM_GERACOES` além de ~16000 traz pouco ganho, pois a busca já estabilizou. Ajustar as taxas de mutação afeta o equilíbrio entre **explorar** novas regiões e **refinar** boas soluções.

---

## 7. Rodando com sua própria matriz de pontos

Para usar o AG com um problema arbitrário (ex.: um drone de entregas numa grade), descreva os pontos numa matriz de texto e converta-a para o formato de distâncias.

Formato de entrada (primeira linha = `linhas colunas`):

```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

- `R` = origem/retorno (obrigatório, único);
- `A`, `B`, `C`, … = pontos de entrega;
- `0` = posição vazia.

**Passo 1 — converter.** Gere um arquivo **com nome diferente** de `edgesbrasil58.tsp` (assim você não sobrescreve a instância oficial):

```bash
python conversorMatrizParaDistancias.py exemplo_entrada.txt meu_problema.tsp
```

O conversor calcula distâncias **euclidianas** entre os pontos e salva no formato de matriz triangular superior.

**Passo 2 — apontar o AG** para esse arquivo via variável de ambiente `ARQUIVO_TSP`:

```powershell
# PowerShell (Windows)
$env:ARQUIVO_TSP = "meu_problema.tsp"
python algoritmoGeneticoBrasil58.py
```

```bash
# bash (Linux/macOS)
ARQUIVO_TSP=meu_problema.tsp python algoritmoGeneticoBrasil58.py
```

Sem a variável, o AG roda o Brasil58 normalmente. O `lerBrasil58.py` detecta o número de cidades pelo próprio arquivo, sem precisar mexer em nenhuma constante.

---

## 8. Testes automatizados

O projeto inclui uma suíte de testes em **[pytest](https://docs.pytest.org/)** que valida desde os operadores individuais até a resolução completa de problemas.

### Instalação e execução

```bash
pip install pytest          # única dependência (só para os testes)
pytest                      # rode a partir da raiz do projeto
```

A saída mostra **logs didáticos** inline (um resumo por teste, sem o "flood" de gerações do AG, que roda em modo silencioso nos testes):

```
tests/test_integracao.py::test_resolve_brazil58_chega_perto_do_otimo
  Brasil58 (800 ger): custo=26173 | otimo=25395 | gap=3.1%
PASSED
tests/test_integracao.py::test_resolve_grade_convertida_bate_forca_bruta
  Grade 5 pontos ['A', 'B', 'C', 'D', 'R']: GA=11 | forca bruta=11
PASSED
```

A suíte roda em ~1 segundo (usa poucas gerações de propósito).

### O que é testado

| Arquivo | Cobertura |
|---|---|
| `tests/test_operadores.py` | Operadores do AG: OX1 e mutações **preservam a permutação**; torneio escolhe o melhor; steady-state **preserva o melhor** e **elimina duplicatas** |
| `tests/test_conversor.py` | Leitura da grade, validações (origem `R` obrigatória, ponto duplicado), distância euclidiana e formato da matriz |
| `tests/test_integracao.py` | **Ponta a ponta**: (1) resolver o **Brasil58** chegando perto do ótimo; (2) converter uma **grade de texto** e resolvê-la, comparando com a **força bruta** (otimo exato) — o "A.G. versus Força Bruta" do projeto |

> **Por que comparar com força bruta?** Nas grades pequenas dá para testar **todas** as rotas e achar o ótimo exato. Assim temos um *gabarito* confiável: o AG **deve** encontrar exatamente esse valor. No Brasil58 isso é inviável (10⁷⁶ rotas), então verificamos a **proximidade** do ótimo conhecido (25395).

---

## 9. Referências rápidas

- **TSP**: https://en.wikipedia.org/wiki/Travelling_salesman_problem
- **Seleção steady-state / (μ+λ)**: Whitley, D. (1989) — *The GENITOR Algorithm*
- **Order Crossover (OX1)**: Davis, L. (1985)
- **2-opt / Inversion**: Croes, G. A. (1958)
