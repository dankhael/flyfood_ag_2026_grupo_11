# 📊 Visualização do Processo Steady State

## Comparação Visual: Geracional vs Steady State

### MODELO GERACIONAL (Original)

```
GERAÇÃO 0:
┌─────────────────────────────────────────┐
│ População: [Ind1, Ind2, Ind3, Ind4]     │
│ Custos:    [100,  95,   110,  105]      │
└─────────────────────────────────────────┘
               ↓ (Cria TODOS os filhos)
┌─────────────────────────────────────────┐
│ Filhos: [Filho1, Filho2, Filho3, Filho4]│
│ Custos: [92,    88,    98,    95]       │
└─────────────────────────────────────────┘
               ↓ (Substitui TUDO)
GERAÇÃO 1:
┌─────────────────────────────────────────┐
│ População: [Filho1, Filho2, Filho3, ...] │
│ Custos:    [92,    88,    98,    ...]    │
└─────────────────────────────────────────┘
               ↓
          (Repete)
```

### MODELO STEADY STATE (Novo)

```
GERAÇÃO 0:
┌─────────────────────────────────────────┐
│ População: [Ind1, Ind2, Ind3, Ind4]     │
│ Custos:    [100,  95,   110,  105]      │
└─────────────────────────────────────────┘
               ↓ (Cria ALGUNS filhos)
┌─────────────────────────────────────────┐
│ Filhos: [Filho1, Filho2]                │
│ Custos: [92,    88]                     │
└─────────────────────────────────────────┘
               ↓ (Mescla com população)
┌──────────────────────────────────────────────┐
│ Mesclada: [Ind1,  Ind2,  Ind3, Ind4, F1, F2] │
│ Custos:   [100,   95,   110, 105, 92, 88]    │
└──────────────────────────────────────────────┘
               ↓ (Seleciona 4 melhores via torneio)
GERAÇÃO 1:
┌─────────────────────────────────────────┐
│ Pop Nova: [F2, Filho1, Ind2, Ind1]      │
│ Custos:   [88,  92,    95,   100]       │
└─────────────────────────────────────────┘
               ↓ (Cria ALGUNS filhos)
           (Repete)
```

---

## 🔄 Processo Detalhado do Steady State

### Passo 1: Inicializar

```
ENTRADA:
- População atual: P = [p1, p2, p3, p4] (tamanho = 4)
- Aptidões: A = [100, 95, 110, 105]

AÇÃO:
Gera num_filhos = tamanho / 2 = 2 filhos
```

### Passo 2: Gerar Filhos

```
PARA i = 1 até 2:
  1. Selecionar Pai1 via torneio
     - Sorteia 3 indivíduos: p2(95), p3(110), p1(100)
     - Melhor: p2(95) ← Pai1

  2. Selecionar Pai2 via torneio
     - Sorteia 3 indivíduos: p4(105), p1(100), p3(110)
     - Melhor: p1(100) ← Pai2

  3. Crossover OX1
     - Cria Filho1 a partir de p2 e p1
     - Cria Filho2 a partir de p1 e p2

  4. Mutação
     - Aplica inversion com probabilidade
     - Aplica scramble com probabilidade

RESULTADO:
Filhos = [f1(custo=92), f2(custo=88)]
```

### Passo 3: Mesclar

```
ENTRADA:
- População: [p1(100), p2(95), p3(110), p4(105)]
- Filhos:    [f1(92), f2(88)]

MESCLADA:
[p1(100), p2(95), p3(110), p4(105), f1(92), f2(88)]
                                    ↑ Novos indivíduos
```

### Passo 4: Selecionar Sobreviventes

```
OBJETIVO: Reduzir população mesclada de 6 para 4

PARA cada posição (1 até 4):

  1ª SELEÇÃO:
    - Sorteia 3 da população mesclada: f2(88), p3(110), p2(95)
    - Melhor: f2(88) ← ENTRA
    - Remove f2 da disponível
    - Nova população: [f2]

  2ª SELEÇÃO:
    - Sorteia 3 restantes: f1(92), p2(95), p1(100)
    - Melhor: f1(92) ← ENTRA
    - Remove f1 da disponível
    - Nova população: [f2, f1]

  3ª SELEÇÃO:
    - Sorteia 3 restantes: p2(95), p3(110), p4(105)
    - Melhor: p2(95) ← ENTRA
    - Remove p2 da disponível
    - Nova população: [f2, f1, p2]

  4ª SELEÇÃO:
    - Sorteia 3 restantes: p1(100), p4(105), p3(110)
    - Melhor: p1(100) ← ENTRA
    - Remove p1 da disponível
    - Nova população: [f2, f1, p2, p1]

RESULTADO FINAL:
População: [f2(88), f1(92), p2(95), p1(100)]
           ↑Novo melhor  ↑Novo 2º melhor
```

### Passo 5: Próxima Geração

```
GERAÇÃO 1:
População: [f2(88), f1(92), p2(95), p1(100)]

VOLTA AO PASSO 2:
Gera 2 novos filhos a partir desta população...
```

---

## 📈 Evolução da População

### Exemplo Completo (4 gerações)

```
GERAÇÃO 0:
│ Populacao: [100, 95, 110, 105]
│ Melhor: 95
│
├─ Cria filhos: [92, 88]
├─ Mescla: [100, 95, 110, 105, 92, 88]
├─ Seleciona: [88, 92, 95, 100]
│
↓ Melhor: 88

GERAÇÃO 1:
│ Populacao: [88, 92, 95, 100]
│ Melhor: 88
│
├─ Cria filhos: [85, 90]
├─ Mescla: [88, 92, 95, 100, 85, 90]
├─ Seleciona: [85, 88, 90, 92]
│
↓ Melhor: 85

GERAÇÃO 2:
│ Populacao: [85, 88, 90, 92]
│ Melhor: 85
│
├─ Cria filhos: [84, 86]
├─ Mescla: [85, 88, 90, 92, 84, 86]
├─ Seleciona: [84, 85, 86, 88]
│
↓ Melhor: 84

GERAÇÃO 3:
│ Populacao: [84, 85, 86, 88]
│ Melhor: 84
│
├─ Cria filhos: [83, 85]
├─ Mescla: [84, 85, 86, 88, 83, 85]
├─ Seleciona: [83, 84, 85, 85]
│
↓ Melhor: 83
```

---

## 🎯 Fluxo de Dados no Código

```python
algoritmoGeneticoSteadyState()
│
├─ Inicializa população
│  │
│  └─ populacao = [ind1, ind2, ...]
│     aptidoes = [100, 95, ...]
│
├─ PARA cada geração:
│  │
│  ├─ Gera filhos (50% da população)
│  │  │
│  │  └─ filhos = [f1, f2, ...]
│  │
│  ├─ ╔═══════════════════════════════════════╗
│  │  ║ SELECAO_SOBREVIVENTES (STEADY STATE) ║
│  │  ╚═══════════════════════════════════════╝
│  │  │
│  │  ├─ Calcula aptidões dos filhos
│  │  │  aptidoes_filhos = [92, 88, ...]
│  │  │
│  │  ├─ Mescla população + filhos
│  │  │  pop_mesclada = [100, 95, 110, 105, 92, 88]
│  │  │
│  │  ├─ Seleciona via torneio
│  │  │  PARA cada posição:
│  │  │    - Sorteia k indivíduos
│  │  │    - Seleciona melhor
│  │  │    - Remove da disponível
│  │  │
│  │  └─ Retorna população reduzida
│  │     populacao = [88, 92, 95, 100]
│  │
│  ├─ Atualiza melhor encontrado
│  │  SE melhor_atual < melhor_global:
│  │     melhor_global = melhor_atual
│  │
│  └─ Imprime progresso
│
└─ Retorna melhor solução encontrada
```

---

## 🔬 Comparação Lado a Lado

```
FUNÇÃO                  | GERACIONAL      | STEADY STATE
─────────────────────────┼─────────────────┼──────────────
Tamanho da população    │ N               │ N
Filhos por geração      │ N               │ N/2
Seleção sobreviventes   │ Elitismo        │ Torneio
Teste mesclagem         │ Não             │ SIM ← Aqui!
Pressão seletiva        │ Baixa           │ Alta
Velocidade convergência │ Lenta           │ Rápida
Diversidade final       │ Maior           │ Menor
Avaliações fitness      │ N * gerações    │ N/2 * gerações
```

---

## 💾 Estrutura de Dados

### Antes da Mesclagem

```
populacao = [p1, p2, p3, p4]        # tamanho = 4
aptidoes = [100, 95, 110, 105]      # 4 valores

filhos = [f1, f2]                   # tamanho = 2
aptidoes_filhos = [92, 88]          # 2 valores
```

### Depois da Mesclagem

```
populacao_mesclada = [p1, p2, p3, p4, f1, f2]      # tamanho = 6
aptidoes_mescladas = [100, 95, 110, 105, 92, 88]   # 6 valores
```

### Depois da Seleção

```
populacao = [f2, f1, p2, p1]            # tamanho = 4 (volta ao original)
aptidoes = [88, 92, 95, 100]            # 4 valores
```

---

## 🎓 Resumo Visual

```
GERACIONAL:
┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐
│Population│─→│ Cria TODOS │─→│Substitui │─→│Population│
│  Gen N   │  │   filhos   │  │   TUDO   │  │ Gen N+1  │
└──────────┘  └────────────┘  └──────────┘  └──────────┘

STEADY STATE:
┌──────────┐  ┌────────────┐  ┌─────────┐  ┌────────┐  ┌──────────┐
│Population│─→│ Cria ALGUNS│─→│  Mescla │─→│Seleciona│─→│Population│
│  Gen N   │  │   filhos   │  │ + Filhos│  │(Torneio)│  │ Gen N+1  │
└──────────┘  └────────────┘  └─────────┘  └────────┘  └──────────┘
                                              ↑
                                         NOVIDADE!
```

---

_Criado: May 27, 2026_  
_Status: ✅ Documentado_
