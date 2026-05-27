# Conversor de Matriz de Pontos para Matriz de Distâncias TSP

## Descrição

Script Python que converte um arquivo no formato de **matriz de pontos de entrega** para o formato **matriz triangular superior de distâncias** (UPPER_ROW) compatível com o algoritmo genético e problema do Caixeiro Viajante (TSP).

## Formato de Entrada

O arquivo de entrada deve seguir este formato:

```
<linhas> <colunas>
<matriz com '0' para vazio e letras para pontos>
```

### Elementos da Matriz
- `R` = Origem e retorno do drone (obrigatório, único)
- `A`, `B`, `C`, `D`, ... = Pontos de entrega (letras maiúsculas)
- `0` = Posição vazia (espaço sem ponto de entrega)

### Exemplo de Entrada (exemplo_entrada.txt)

```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

Neste exemplo:
- Matriz 4x5
- R (origem) está na posição (3, 0)
- A está em (1, 1)
- B está em (3, 2)
- C está em (2, 4)
- D está em (0, 4)

## Formato de Saída

O conversor gera **dois arquivos**:

### 1. Arquivo TSP Completo (`.tsp`)
Formato padrão para problemas de otimização com cabeçalho:

```
NAME: [nome_do_problema]
TYPE: TSP
DIMENSION: [número_de_cidades]
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: UPPER_ROW
EDGE_WEIGHT_SECTION
[matriz triangular superior de distâncias]
```

### 2. Arquivo EDGES Simplificado (`.tsp`)
Contém apenas a matriz triangular superior de distâncias, compatível com `lerBrasil58.py`

## Como Usar

### Uso Básico

```bash
python conversorMatrizParaDistancias.py <arquivo_entrada>
```

Isso gera automaticamente:
- `<arquivo_entrada>_distancias.tsp` (formato TSP completo)
- `<arquivo_entrada>_edges.tsp` (formato simplificado)

### Exemplo

```bash
python conversorMatrizParaDistancias.py exemplo_entrada.txt
```

Saída:
```
✓ Arquivo TSP salvo com sucesso em: exemplo_entrada_distancias.tsp
✓ Arquivo EDGES salvo com sucesso em: exemplo_entrada_edges.tsp
```

### Uso com Nomes Customizados

```bash
python conversorMatrizParaDistancias.py entrada.txt saida.tsp saida_edges.tsp
```

## Cálculo de Distâncias

As distâncias são calculadas usando a **fórmula da distância euclidiana**:

```
d = √((y₂ - y₁)² + (x₂ - x₁)²)
```

Onde:
- (y₁, x₁) e (y₂, x₂) são as coordenadas dos dois pontos
- A distância é arredondada para o inteiro mais próximo

## Ordenação das Cidades

As cidades são automaticamente ordenadas da seguinte forma:

1. `R` (origem) recebe índice 1
2. Demais pontos (A, B, C, ...) recebem índices em ordem alfabética

No exemplo acima, a ordem seria: **R, A, B, C, D** (índices 1-5)

## Integração com o Algoritmo Genético

O arquivo de saída EDGES (formato simplificado) pode ser utilizado diretamente pelo script `lerBrasil58.py`:

```python
from lerBrasil58 import distancias, custoCaminho
# Substitua 'edgesbrasil58.tsp' pela saída do conversor
```

Basta alterar o nome do arquivo na leitura de `lerBrasil58.py`:

```python
objArq = open("exemplo_entrada_edges.tsp")  # seu arquivo convertido
```

## Validações

O conversor realiza as seguintes validações:

✓ Verifica se o arquivo existe  
✓ Verifica se a dimensão da matriz é consistente  
✓ Verifica se existe exatamente um ponto de origem `R`  
✓ Detecta pontos duplicados  
✓ Calcula corretamente as distâncias euclidianas  

## Exemplos de Uso

### Criar um novo problema de entrega

1. Crie um arquivo `entregas.txt`:

```
6 6
0 0 0 A 0 0
0 0 0 0 0 0
B 0 0 0 0 C
0 0 0 0 0 0
0 D 0 0 0 0
R 0 E 0 0 F
```

2. Converta:

```bash
python conversorMatrizParaDistancias.py entregas.txt
```

3. Use com o algoritmo genético modificando `lerBrasil58.py`:

```python
objArq = open("entregas_edges.tsp")
```

## Limitações

- Máximo de cidades: teoricamente ilimitado (limitado por memória)
- Pontos devem ser representados por **letras maiúsculas** (A-Z, etc.)
- Deve haver **exatamente um ponto R** (origem)
- Matriz não precisa estar quadrada
- Distâncias são calculadas em linha reta (euclidiana 2D)

## Arquivos Gerados no Exemplo

Ao executar `python conversorMatrizParaDistancias.py exemplo_entrada.txt`, são criados:

- **exemplo_entrada_distancias.tsp** - Formato TSP completo com cabeçalho
- **exemplo_entrada_edges.tsp** - Matriz de distâncias simplificada

Ambos contêm os mesmos dados de distância, apenas em formatos diferentes.
