# FlyFood AG 2026 — Brasil58 (TSP com Algoritmo Genético)

Resolução do problema do **Caixeiro Viajante (TSP)** sobre a instância **Brasil58** (58 cidades brasileiras) utilizando um **Algoritmo Genético (AG)**.

---

## 1. O problema do Caixeiro Viajante (TSP)

Dado um conjunto de cidades e as distâncias entre cada par delas, o objetivo é encontrar a **rota de menor custo** que:

- Passa por **todas** as cidades exatamente uma vez;
- Retorna à cidade de origem ao final.

Matematicamente, é um problema **NP-difícil**: o número de rotas possíveis cresce com `(n-1)!/2`. Para 58 cidades, isso significa aproximadamente 10⁷⁶ rotas — inviável testar todas. Por isso usamos **meta-heurísticas** como o AG, que não garantem o ótimo, mas encontram boas soluções em tempo razoável.

### A instância Brasil58

- 58 cidades brasileiras
- Distâncias armazenadas em formato de **matriz triangular superior** no arquivo `edgesbrasil58.tsp`
- Ótimo conhecido: **25395**

---

## 2. Estrutura do projeto

| Arquivo | Função |
|---|---|
| `edgesbrasil58.tsp` | Dados das distâncias entre cidades |
| `lerBrasil58.py` | Lê o arquivo, monta o dicionário de distâncias, define funções de custo e inicialização |
| `algoritmoGeneticoBrasil58.py` | Loop principal do AG com seleção, crossover e mutação |

---

## 3. Conceitos do código

### 3.1 Representação do indivíduo

Cada **indivíduo** (uma rota candidata) é uma **permutação** das cidades 1 a 58:

```python
individuo = [5, 14, 2, 3, 7, ...]   # passa por 5, depois 14, depois 2...
```

A **população** é uma lista de indivíduos.

### 3.2 Função de aptidão (fitness)

A função `custoCaminho` soma as distâncias entre cidades consecutivas e adiciona o retorno à origem:

```
custo = d(p0, p1) + d(p1, p2) + ... + d(pn-1, pn) + d(pn, p0)
```

Como queremos **minimizar** o custo, indivíduos com **menor custo são melhores**.

### 3.3 Seleção de pais — Torneio (k=3)

A cada novo filho que precisa ser gerado, sorteamos `k` indivíduos da população e o de **menor custo vence** o torneio. Vantagens:

- Não exige normalizar fitness (importante para problemas de minimização)
- A "pressão seletiva" é controlada por `k`: maior `k` favorece os melhores; menor `k` mantém diversidade

### 3.4 Crossover — Order Crossover (OX1)

Crossovers tradicionais quebrariam a permutação (gerando rotas com cidades repetidas/ausentes). O **OX1** preserva a propriedade de permutação:

1. Sorteia um trecho `[a..b]` no pai1 e copia para o filho;
2. Percorre o pai2 a partir de `b+1` (de forma circular), preenchendo as posições restantes do filho **na ordem em que aparecem no pai2**, ignorando genes já presentes no trecho copiado.

Resultado: o filho herda uma **subsequência contígua** do pai1 e a **ordem relativa** das demais cidades do pai2.

### 3.5 Mutações

Duas mutações com taxas independentes:

**Inversion** — inverte um trecho aleatório:
```
[1 2 3 4 5 6 7]  →  [1 2 6 5 4 3 7]
```
É a base do clássico **2-opt** em TSP. Preserva quase todas as arestas adjacentes, alterando apenas duas — modificação local e eficaz.

**Scramble** — embaralha um trecho aleatório:
```
[1 2 3 4 5 6 7]  →  [1 2 5 3 6 4 7]
```
Mais disruptiva. Útil para **escapar de ótimos locais** quando a população começa a convergir prematuramente.

### 3.6 Elitismo

Antes de gerar a nova população, os `TAMANHO_ELITE` melhores indivíduos são **copiados diretamente** para a próxima geração. Isso garante que o melhor encontrado nunca se perca por azar nos operadores genéticos.

### 3.7 Loop geracional

```
inicializa população aleatória
calcula aptidão
repete por NUM_GERACOES:
    seleciona elite e copia para nova geração
    enquanto nova geração não estiver cheia:
        pai1 = torneio
        pai2 = torneio
        filhos = crossover(pai1, pai2)
        aplica mutações
        adiciona filhos
    substitui população
    atualiza melhor global
```

---

## 4. Parâmetros configuráveis

No topo de `algoritmoGeneticoBrasil58.py`:

| Parâmetro | Valor padrão | Efeito |
|---|---|---|
| `TAMANHO_POPULACAO` | 150 | Mais = exploração maior, porém mais lento |
| `NUM_GERACOES` | 1000 | Critério de parada |
| `TAXA_CROSSOVER` | 0.9 | Probabilidade de aplicar OX1 |
| `TAXA_MUT_INVERSAO` | 0.2 | Probabilidade de inverter trecho |
| `TAXA_MUT_SCRAMBLE` | 0.05 | Probabilidade de embaralhar trecho |
| `TAMANHO_TORNEIO` | 3 | Pressão seletiva |
| `TAMANHO_ELITE` | 2 | Quantos melhores passam direto |

---

## 5. Como executar

```bash
python algoritmoGeneticoBrasil58.py
```

A cada 50 gerações o programa imprime o melhor custo atual e o melhor global. Ao final, imprime a rota encontrada e seu custo.

---

## 6. Referências rápidas

- **TSP**: https://en.wikipedia.org/wiki/Travelling_salesman_problem
- **Order Crossover (OX1)**: Davis, L. (1985)
- **2-opt / Inversion**: Croes, G. A. (1958)
