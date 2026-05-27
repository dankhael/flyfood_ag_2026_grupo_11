# ⚡ Guia Rápido: Executar Diferentes Modelos

## 🎯 Três Formas de Executar

### Opção 1: Modelo Geracional (Original - Padrão)

```bash
python algoritmoGeneticoBrasil58.py
```

**O que muda no código:**
Nenhuma mudança necessária - é a opção padrão!

---

### Opção 2: Modelo Steady State (Novo)

Edite `algoritmoGeneticoBrasil58.py` - seção `if __name__ == "__main__":`:

**Antes:**

```python
if __name__ == "__main__":
    random.seed()

    # ===== ESCOLHA QUAL MODELO USAR =====

    # Opção 1: Modelo Geracional (Original)
    print("\n[1/3] Executando Algoritmo Genético - MODELO GERACIONAL")
    melhorRota, melhorCusto = algoritmoGenetico()  # ← ESTE
```

**Depois:**

```python
if __name__ == "__main__":
    random.seed()

    # ===== ESCOLHA QUAL MODELO USAR =====

    # Opção 2: Modelo Steady State
    print("\n[1/2] Executando Algoritmo Genético - MODELO STEADY STATE")
    melhorRota, melhorCusto = algoritmoGeneticoSteadyState()  # ← MUDE PARA ESTE
```

Execute:

```bash
python algoritmoGeneticoBrasil58.py
```

---

### Opção 3: Comparar Ambos os Modelos

Edite `algoritmoGeneticoBrasil58.py`:

**Altere para:**

```python
if __name__ == "__main__":
    random.seed()

    # Opção 3: Comparar ambos os modelos
    algoritmoGeneticoHibrido()  # ← USE ESTE
    melhorRota = None  # Para não imprimir resultado duplicado
```

Execute:

```bash
python algoritmoGeneticoBrasil58.py
```

**Saída esperada:**

```
======================================================================
COMPARAÇÃO DE MODELOS
======================================================================

--- Modelo GERACIONAL (Original) ---
[gerações...]

--- Modelo STEADY STATE ---
[gerações...]

======================================================================
RESULTADO FINAL
======================================================================

Modelo Geracional:
  Custo: 28456
  Rota:  [1, 2, 3, ...]

Modelo Steady State:
  Custo: 27234
  Rota:  [1, 3, 2, ...]

Diferença: -1222
======================================================================
```

---

## 📋 Resumo das Opções

| Opção | Função                           | Arquivo                        | Características            |
| ----- | -------------------------------- | ------------------------------ | -------------------------- |
| 1     | `algoritmoGenetico()`            | `algoritmoGeneticoBrasil58.py` | Geracional, Exploração     |
| 2     | `algoritmoGeneticoSteadyState()` | `algoritmoGeneticoBrasil58.py` | Steady State, Convergência |
| 3     | `algoritmoGeneticoHibrido()`     | `algoritmoGeneticoBrasil58.py` | Compara 1 e 2              |

---

## 🔧 Modificações Rápidas

### Para usar Steady State permanentemente:

```python
# Linha aproximadamente 159 (no if __name__)
# Comente:
# print("\n[1/3] Executando Algoritmo Genético - MODELO GERACIONAL")
# melhorRota, melhorCusto = algoritmoGenetico()

# Descomente:
print("\n[1/2] Executando Algoritmo Genético - MODELO STEADY STATE")
melhorRota, melhorCusto = algoritmoGeneticoSteadyState()
```

---

## 📊 Exemplo: Mudando de Modelo

### Passo 1: Encontre esta seção (linha ~159):

```python
if __name__ == "__main__":
    random.seed()  # remova o seed ou fixe para reproduzir

    # ===== ESCOLHA QUAL MODELO USAR =====

    # Opção 1: Modelo Geracional (Original)
    print("\n[1/3] Executando Algoritmo Genético - MODELO GERACIONAL")
    melhorRota, melhorCusto = algoritmoGenetico()

    # Opção 2: Modelo Steady State
    # print("\n[1/2] Executando Algoritmo Genético - MODELO STEADY STATE")
    # melhorRota, melhorCusto = algoritmoGeneticoSteadyState()
```

### Passo 2: Troque os comentários:

```python
if __name__ == "__main__":
    random.seed()

    # Opção 2: Modelo Steady State
    print("\n[1/2] Executando Algoritmo Genético - MODELO STEADY STATE")
    melhorRota, melhorCusto = algoritmoGeneticoSteadyState()

    # Opção 1: Modelo Geracional (Original)
    # print("\n[1/3] Executando Algoritmo Genético - MODELO GERACIONAL")
    # melhorRota, melhorCusto = algoritmoGenetico()
```

### Passo 3: Execute:

```bash
python algoritmoGeneticoBrasil58.py
```

---

## 💡 Qual Escolher?

### Use GERACIONAL se:

- ✓ Quer exploração máxima
- ✓ Problema tem múltiplos ótimos locais
- ✓ Primeira execução / exploração inicial
- ✓ Quer evitar convergência prematura

### Use STEADY STATE se:

- ✓ Quer convergência rápida
- ✓ Já explorou bastante
- ✓ Busca otimização fina
- ✓ Tempo é limitado

### Use HÍBRIDO se:

- ✓ Quer comparar os dois
- ✓ Quer escolher o melhor resultado
- ✓ Quer entender diferenças

---

## 🚀 Recomendação

Para o **TSP Brasil58**, recomendo:

**Primeira execução:**

```bash
algoritmoGenetico()  # Geracional - explora bem
```

**Otimização:**

```bash
algoritmoGeneticoSteadyState()  # Converge mais rápido
```

**Comparação:**

```bash
algoritmoGeneticoHibrido()  # Vê qual é melhor
```

---

## 📝 Mudanças Implementadas

✅ Adicionada função `selecaoSobreviventes()` - Merge e seleção steady state  
✅ Adicionada função `algoritmoGeneticoSteadyState()` - Novo modelo  
✅ Adicionada função `algoritmoGeneticoHibrido()` - Comparação  
✅ Atualizado `if __name__ == "__main__"` - Com opções comentadas

---

_Guia criado: May 27, 2026_
