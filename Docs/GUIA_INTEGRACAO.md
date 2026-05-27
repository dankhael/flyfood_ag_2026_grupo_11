# Guia de Integração: Conversor + Algoritmo Genético

## Visão Geral

Este guia mostra como usar o conversor de matriz para distâncias em conjunto com o algoritmo genético para resolver problemas de roteamento de drone.

## Fluxo de Trabalho Completo

```
┌─────────────────────┐
│ Matriz de Pontos    │
│ (entrada.txt)       │
│ R, A, B, C, D...    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│ conversorMatrizParaDistancias   │
│ (script de conversão)           │
└──────────┬──────────────────────┘
           │
           ├─────────────────────────────┐
           │                             │
           ▼                             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │ _distancias.tsp  │        │ _edges.tsp       │
    │ (formato TSP)    │        │ (simplificado)   │
    └──────────────────┘        └────────┬─────────┘
                                         │
                                         ▼
                          ┌──────────────────────────┐
                          │ lerBrasil58.py           │
                          │ (lê distâncias)          │
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │ algoritmoGeneticoBrasil │
                          │ (resolve o problema)    │
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │ Solução Otimizada        │
                          │ (melhor rota)            │
                          └──────────────────────────┘
```

## Passo a Passo

### 1. Criar o Arquivo de Entrada

Crie um arquivo de texto (ex: `minha_entrega.txt`) com a matriz de pontos:

```txt
5 6
0 A 0 0 0 0
0 0 0 0 0 B
C 0 0 0 0 0
0 0 0 D 0 0
R 0 0 0 E 0
```

**Dicas:**
- A primeira linha contém: `<número_de_linhas> <número_de_colunas>`
- Separe os elementos com espaços
- Use apenas `R` (uma única origem), `A-Z` (pontos de entrega) e `0` (vazio)

### 2. Executar o Conversor

```bash
python conversorMatrizParaDistancias.py minha_entrega.txt
```

**Saída esperada:**
```
============================================================
Conversor de Matriz de Pontos para Distâncias TSP
============================================================

1. Lendo arquivo: minha_entrega.txt
   ✓ 6 pontos encontrados
      R: linha 4, coluna 0
      A: linha 0, coluna 1
      B: linha 1, coluna 5
      C: linha 2, coluna 0
      D: linha 3, coluna 3
      E: linha 4, coluna 4

2. Calculando matriz de distâncias...
   ✓ Matriz calculada com sucesso
   Cidades ordenadas: R, A, B, C, D, E

3. Salvando arquivos de saída...
✓ Arquivo TSP salvo com sucesso em: minha_entrega_distancias.tsp
✓ Arquivo EDGES salvo com sucesso em: minha_entrega_edges.tsp

============================================================
Conversão concluída com sucesso!
============================================================
```

### 3. Preparar o Algoritmo Genético

Crie um novo arquivo `algoritmoGeneticoPrincipal.py` ou modifique `lerBrasil58.py`:

#### Opção A: Modificar lerBrasil58.py

Altere a linha:
```python
objArq = open("edgesbrasil58.tsp")
```

Para:
```python
objArq = open("minha_entrega_edges.tsp")  # seu arquivo convertido
```

E ajuste as constantes no `algoritmoGeneticoBrasil58.py`:

```python
QTDE_CIDADES      = 6  # número de pontos (incluindo R)
TAMANHO_POPULACAO = 100  # ajuste conforme necessário
NUM_GERACOES      = 500   # ajuste conforme necessário
```

#### Opção B: Criar Script Parametrizado (Recomendado)

Crie `algoritmoGeneticoFlexivel.py`:

```python
import sys
import random
from lerBrasil58 import distancias, custoCaminho, inicializaPopulacao, calculaAptidao

# Importa operadores do algoritmo genético original
# (copie as funções do algoritmoGeneticoBrasil58.py)

def resolver_tsp_para_arquivo(arquivo_distancias, num_cidades, 
                              tamanho_populacao=150, 
                              num_geracoes=1000,
                              arquivo_saida="resultado.txt"):
    """
    Resolve o TSP para um arquivo de distâncias especificado.
    
    Args:
        arquivo_distancias: caminho do arquivo _edges.tsp
        num_cidades: número de cidades no problema
        tamanho_populacao: tamanho da população
        num_geracoes: número de gerações
        arquivo_saida: arquivo para salvar resultado
    """
    
    # Lê distâncias do arquivo
    objArq = open(arquivo_distancias)
    distancias = {}
    
    for i in range(1, num_cidades):
        linha = objArq.readline()
        lista = linha.split()
        for j in range(i+1, num_cidades + 1):
            if len(lista) > 0:
                peso = int(lista.pop(0))
            else:
                print(f"Erro na linha {i}")
                return None
            distancias[(i,j)] = peso
            distancias[(j,i)] = peso
    
    objArq.close()
    
    # Executa algoritmo genético
    # ... (copie o código principal do algoritmoGeneticoBrasil58.py)
    
    # Salva resultado
    with open(arquivo_saida, 'w') as f:
        f.write(f"Arquivo de entrada: {arquivo_distancias}\n")
        f.write(f"Número de cidades: {num_cidades}\n")
        f.write(f"Melhor custo: {melhorCusto}\n")
        f.write(f"Rota: {melhorRota}\n")
    
    return melhorRota, melhorCusto

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python algoritmoGeneticoFlexivel.py <arquivo_edges.tsp> [num_cidades]")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    num_cidades = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    resultado = resolver_tsp_para_arquivo(arquivo, num_cidades)
```

### 4. Executar o Algoritmo

```bash
# Usando arquivo modificado
python algoritmoGeneticoBrasil58.py

# Ou usando versão flexível
python algoritmoGeneticoFlexivel.py minha_entrega_edges.tsp 6
```

### 5. Analisar Resultado

O algoritmo genético produzirá:

```
Geracao    0 | melhor atual: 28 | melhor global: 28
Geracao   50 | melhor atual: 24 | melhor global: 24
Geracao  100 | melhor atual: 22 | melhor global: 22
...
Geracao  999 | melhor atual: 18 | melhor global: 18

=== Resultado final ===
Custo: 18
Rota:  [1, 2, 5, 3, 4, 6]
```

**Interpretação:**
- Índice 1 = R (origem)
- Índice 2 = A (primeiro ponto de entrega)
- Índice 5 = E (segundo ponto)
- etc.

## Arquivos Criados

```
minha_entrega.txt                 → Arquivo de entrada (matriz de pontos)
minha_entrega_distancias.tsp      → Arquivo TSP completo
minha_entrega_edges.tsp           → Matriz de distâncias (para lerBrasil58.py)
```

## Exemplo Completo

### 1. Criar arquivo de entrada

```bash
cat > entrega_semanal.txt << 'EOF'
10 10
0 0 A 0 0 0 B 0 0 0
0 0 0 0 0 0 0 0 0 0
C 0 0 0 0 0 0 0 D 0
0 0 0 0 E 0 0 0 0 0
0 0 0 0 0 0 0 0 0 F
R 0 0 0 0 0 0 0 0 0
0 0 G 0 0 0 0 0 0 0
0 0 0 0 0 H 0 0 0 0
0 I 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 J
EOF
```

### 2. Converter

```bash
python conversorMatrizParaDistancias.py entrega_semanal.txt
```

### 3. Adaptar algoritmo

```bash
# Editar lerBrasil58.py ou criar novo arquivo
# Mudar objArq = open("edgesbrasil58.tsp")
# Para objArq = open("entrega_semanal_edges.tsp")

# Editar algoritmoGeneticoBrasil58.py
QTDE_CIDADES = 11  # 1 origem + 10 pontos (A-J)
```

### 4. Executar

```bash
python algoritmoGeneticoBrasil58.py
```

## Troubleshooting

### Erro: "ponto 'R' duplicado"
- Verifique se há apenas um `R` na matriz
- Limpe espaços extras

### Erro: "ponto de origem 'R' não encontrado"
- Adicione um `R` em alguma posição da matriz
- Certifique-se de que é exatamente `R` (maiúscula)

### Distâncias muito grandes ou pequenas
- Verifique se a posição dos pontos está correta
- Cidades muito próximas terão distâncias pequenas
- A distância é calculada em unidades de grid (linha/coluna)

### O algoritmo não converge
- Aumente `NUM_GERACOES`
- Verifique se `TAMANHO_POPULACAO` é apropriado
- Ajuste as taxas de mutação

## Performance

Para diferentes tamanhos de problema:

| Pontos | População | Gerações | Tempo (aprox) |
|--------|-----------|----------|---------------|
| 5-10   | 50        | 500      | < 1s          |
| 10-20  | 100       | 1000     | 1-5s          |
| 20-50  | 200       | 2000     | 10-30s        |
| 50+    | 300+      | 5000+    | > 1 min       |

## Dicas Finais

✓ Comece com exemplos pequenos (5-10 pontos)  
✓ Valide visualmente se a rota faz sentido  
✓ Salve configurações que funcionam bem  
✓ Documente o problema e a solução  
✓ Use versionamento (git) para rastrear mudanças
