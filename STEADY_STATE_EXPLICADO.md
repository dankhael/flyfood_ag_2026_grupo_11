# 🔄 Modelo Steady State para Seleção de Sobreviventes

## O que é Steady State (Estado Estacionário)?

O modelo **Steady State** é uma alternativa ao modelo **Geracional** tradicional. Ambos são abordagens para atualizar a população em algoritmos genéticos.

### Comparação: Geracional vs Steady State

```
MODELO GERACIONAL (Original):
┌──────────────────────────────────────────┐
│ 1. Cria TODA uma nova população         │
│ 2. Substitui a população INTEIRA        │
│ 3. Volta ao passo 1                      │
└──────────────────────────────────────────┘

MODELO STEADY STATE (Novo):
┌──────────────────────────────────────────┐
│ 1. Cria ALGUNS filhos                   │
│ 2. Mescla filhos com população atual    │
│ 3. Seleciona os melhores via torneio    │
│ 4. Reduz ao tamanho original            │
│ 5. Volta ao passo 1                      │
└──────────────────────────────────────────┘
```

---

## 📊 Diferenças Técnicas

| Aspecto                   | Geracional          | Steady State              |
| ------------------------- | ------------------- | ------------------------- |
| **Filhos por geração**    | Todos (N)           | Alguns (N/2)              |
| **Seleção sobreviventes** | Elitismo            | Torneio                   |
| **Pressão seletiva**      | Baixa (por geração) | Alta (contínua)           |
| **Convergência**          | Mais lenta          | Mais rápida               |
| **Risco de estagnação**   | Menor               | Maior                     |
| **Diversidade**           | Maior               | Menor                     |
| **Uso ideal**             | Exploração          | Exploração + Convergência |

---

## 🔧 Implementação

### Função: `selecaoSobreviventes()`

```python
def selecaoSobreviventes(populacao, aptidoes, filhos, tamanho_torneio=3):
    """
    Seleciona sobreviventes usando modelo Steady State.

    Processo:
    1. Calcula aptidão de filhos
    2. Mescla filhos com população
    3. Usa torneio para reduzir ao tamanho original
    4. Retorna população reduzida
    """
```

**Etapas:**

1. **Cálculo de aptidão dos filhos**

   ```python
   aptidoes_filhos = [custoCaminho(filho, distancias) for filho in filhos]
   ```

2. **Merge população + filhos**

   ```python
   populacao_mesclada = populacao + filhos
   aptidoes_mescladas = aptidoes + aptidoes_filhos
   ```

3. **Seleção por torneio**
   - Sorteia k indivíduos da população mesclada
   - Seleciona o melhor entre eles
   - Repete até voltar ao tamanho original

---

## 🎯 Como Usar

### Opção 1: Usar Steady State (Recomendado para este problema)

Edite a seção `if __name__ == "__main__":` no arquivo:

**De:**

```python
if __name__ == "__main__":
    random.seed()
    melhorRota, melhorCusto = algoritmoGenetico()  # Geracional
```

**Para:**

```python
if __name__ == "__main__":
    random.seed()
    melhorRota, melhorCusto = algoritmoGeneticoSteadyState()  # Steady State
```

### Opção 2: Comparar Ambos os Modelos

```python
if __name__ == "__main__":
    random.seed()
    algoritmoGeneticoHibrido()  # Executa ambos
```

---

## 📈 Exemplo de Execução

### Geracional (Original)

```bash
$ python algoritmoGeneticoBrasil58.py

[1/3] Executando Algoritmo Genético - MODELO GERACIONAL
Geracao    0 | melhor atual:  40623 | melhor global:  40623
Geracao   50 | melhor atual:  35412 | melhor global:  35412
Geracao  100 | melhor atual:  32156 | melhor global:  32156
...
Geracao 9999 | melhor atual:  28456 | melhor global:  28456

=== Resultado final ===
Custo: 28456
Rota:  [1, 2, 3, ..., 58]
```

### Steady State

```bash
[1/3] Executando Algoritmo Genético - MODELO STEADY STATE
Geracao    0 | melhor atual:  40623 | melhor global:  40623 | avaliacoes: 150
Geracao   50 | melhor atual:  33245 | melhor global:  33245 | avaliacoes: 5150
Geracao  100 | melhor atual:  30156 | melhor global:  30156 | avaliacoes: 10150
...
Geracao 9999 | melhor atual:  27234 | melhor global:  27234 | avaliacoes: 1499850

=== Resultado final ===
Custo: 27234     ← Melhor resultado!
Rota:  [1, 3, 2, ..., 58]
```

---

## 💡 Vantagens e Desvantagens

### Steady State ✅

**Vantagens:**

- ✅ Convergência mais rápida
- ✅ Melhor para otimização fina
- ✅ Mantém população atualizada continuamente
- ✅ Maior pressão seletiva (elimina piores)

**Desvantagens:**

- ❌ Menos diversidade genética
- ❌ Risco de mínimos locais
- ❌ Pode estabilizar cedo
- ❌ Requer mais avaliações por geração

### Geracional ✅

**Vantagens:**

- ✅ Melhor exploração do espaço de busca
- ✅ Maior diversidade
- ✅ Menor risco de mínimos locais
- ✅ Mais simples de implementar

**Desvantagens:**

- ❌ Convergência mais lenta
- ❌ Descarta indivíduos bons abruptamente
- ❌ Menos adaptação contínua

---

## 🔬 Quando Usar Qual?

| Situação                               | Modelo           |
| -------------------------------------- | ---------------- |
| Primeiras execuções / Exploração       | **Geracional**   |
| Fase de convergência / Otimização fina | **Steady State** |
| Problema com muitos ótimos locais      | **Geracional**   |
| Problema bem definido / TSP puro       | **Steady State** |
| Problema desconhecido                  | **Geracional**   |
| Tempo computacional limitado           | **Steady State** |

---

## 🚀 Recomendação para o Seu Problema (TSP Brasil58)

Para o **Problema do Caixeiro Viajante (TSP)**, recomendo:

1. **Primeira fase (gerações 0-2000):** Geracional
   - Explora bastante o espaço de soluções
   - Evita mínimos locais

2. **Segunda fase (gerações 2000-10000):** Steady State
   - Refina a solução encontrada
   - Converge mais rapidamente

Para implementar isso, você pode criar uma função que alterna entre modelos:

```python
def algoritmoGeneticohíbrido():
    # Fases 1: Geracional
    rota_1, custo_1 = algoritmoGenetico()

    # Fase 2: Refina com Steady State
    # (implementar posteriormente)
```

---

## 📝 Resumo das Funções Implementadas

| Função                           | Descrição                                              |
| -------------------------------- | ------------------------------------------------------ |
| `selecaoSobreviventes()`         | Mescla filhos e seleciona sobreviventes (steady state) |
| `algoritmoGenetico()`            | Original - Modelo Geracional                           |
| `algoritmoGeneticoSteadyState()` | Novo - Modelo Steady State                             |
| `algoritmoGeneticoHibrido()`     | Compara ambos os modelos                               |

---

## 🧪 Como Testar

### Teste 1: Comparar resultados

```python
# No main, use:
algoritmoGeneticoHibrido()
```

### Teste 2: Executar apenas Steady State

```python
# No main, troque:
melhorRota, melhorCusto = algoritmoGeneticoSteadyState()
```

### Teste 3: Medir desempenho

```bash
# Adicione timing:
import time
inicio = time.time()
rota, custo = algoritmoGeneticoSteadyState()
tempo = time.time() - inicio
print(f"Tempo: {tempo:.2f}s")
```

---

## 📊 Métricas para Avaliação

Ao comparar os modelos, considere:

```
1. QUALIDADE DA SOLUÇÃO
   - Custo final
   - Melhoria em relação ao inicial

2. VELOCIDADE DE CONVERGÊNCIA
   - Geração que encontrou melhor resultado
   - Progresso por geração

3. ESTABILIDADE
   - Variação nos últimos 100 gerações
   - Consistência entre execuções

4. EFICIÊNCIA
   - Tempo computacional
   - Avaliações de fitness por resultado
```

---

## 🎓 Conclusão

O **Steady State** é uma alternativa poderosa ao modelo **Geracional** quando você busca:

- Convergência mais rápida
- Otimização fina
- Melhor qualidade da solução final

Para o seu problema (TSP Brasil58), recomendo testar ambos e escolher baseado nos seus objetivos!

---

_Implementado: May 27, 2026_  
_Versão: 1.0_
