# 📚 Referência Completa do Projeto

## 📦 Arquivos do Projeto

### 🆕 NOVOS ARQUIVOS (Adicionados para conversão)

#### **1. conversorMatrizParaDistancias.py** ⭐
- **Tipo:** Script principal
- **Descrição:** Converte matriz de pontos para matriz triangular de distâncias
- **Entrada:** Arquivo de texto com matriz de pontos (R, A, B, C, ...)
- **Saída:** Dois arquivos de distâncias (.tsp)
- **Uso:** `python conversorMatrizParaDistancias.py entrada.txt`
- **Funcionalidades:**
  - Leitura de matriz com pontos de entrega
  - Cálculo de distância euclidiana entre pontos
  - Geração de matriz triangular superior (UPPER_ROW)
  - Validação e tratamento de erros
  - Suporte a nomes de arquivo customizados

#### **2. teste_conversor.py**
- **Tipo:** Script de testes
- **Descrição:** Executa testes do conversor com múltiplos exemplos
- **Uso:** `python teste_conversor.py`
- **Testa:** Validação dos arquivos gerados

#### **3. exemplo_entrada.txt**
- **Tipo:** Arquivo de exemplo (entrada)
- **Descrição:** Exemplo simples com 5 pontos (R, A, B, C, D)
- **Matriz:** 4x5
- **Gerado automaticamente:**
  - `exemplo_entrada_distancias.tsp` (formato TSP completo)
  - `exemplo_entrada_edges.tsp` (formato simplificado)

#### **4. exemplo_grande.txt**
- **Tipo:** Arquivo de exemplo (entrada)
- **Descrição:** Exemplo complexo com 10 pontos (R, A-J)
- **Matriz:** 8x10

#### **5. RESUMO_CONVERSOR.md** 📖
- **Tipo:** Documentação (este arquivo)
- **Conteúdo:** Resumo rápido de tudo que foi criado
- **Seções:** Início rápido, exemplos, troubleshooting

#### **6. CONVERSOR_README.md** 📖
- **Tipo:** Documentação técnica completa
- **Conteúdo:** 
  - Formato de entrada detalhado
  - Formato de saída explicado
  - Fórmulas de cálculo
  - Validações realizadas
  - Limitações e casos de uso
  - Exemplos avançados

#### **7. GUIA_INTEGRACAO.md** 📖
- **Tipo:** Guia de uso com algoritmo genético
- **Conteúdo:**
  - Fluxo de trabalho completo
  - Passo a passo integração
  - Exemplo prático
  - Troubleshooting
  - Performance e dicas

### 📝 ARQUIVOS ORIGINAIS (Existentes - Não modificados)

#### **algoritmoGeneticoBrasil58.py**
- **Descrição:** Implementa o algoritmo genético para TSP
- **Operadores:**
  - Seleção: Torneio (k=3)
  - Crossover: Order Crossover (OX1)
  - Mutação: Inversion + Scramble
- **Parâmetros:**
  ```python
  QTDE_CIDADES      = 58
  TAMANHO_POPULACAO = 150
  NUM_GERACOES      = 1000
  TAXA_CROSSOVER    = 0.9
  TAXA_MUT_INVERSAO = 0.2
  TAXA_MUT_SCRAMBLE = 0.05
  ```
- **Saída:** Melhor rota encontrada e seu custo total

#### **lerBrasil58.py**
- **Descrição:** Lê arquivo de distâncias e fornece utilitários
- **Funções:**
  - `ler_arquivo()`: Lê matriz de distâncias (UPPER_ROW)
  - `custoCaminho()`: Calcula custo total de uma rota
  - `inicializaPopulacao()`: Cria população inicial
  - `calculaAptidao()`: Avalia fitness de indivíduos
- **Entrada:** Arquivo no formato UPPER_ROW
- **Saída:** Dicionário de distâncias

#### **brazil58.tsp**
- **Tipo:** Arquivo de dados TSP
- **Descrição:** 58 cidades no Brasil (padrão TSPLIB)
- **Formato:** TSP com cabeçalho completo
- **Estrutura:**
  - NAME: brazil58
  - DIMENSION: 58
  - EDGE_WEIGHT_TYPE: EXPLICIT
  - EDGE_WEIGHT_FORMAT: UPPER_ROW

#### **edgesbrasil58.tsp**
- **Tipo:** Arquivo de dados (simplificado)
- **Descrição:** Apenas a matriz triangular superior de distâncias
- **Formato:** 57 linhas de números (sem cabeçalho)
- **Uso:** Lido por `lerBrasil58.py`

#### **README.md**
- **Descrição:** Documentação geral do projeto original

## 🔄 Fluxo de Dados

```
┌────────────────────────────────────┐
│  Matriz de Pontos de Entrega       │
│  (entrada.txt)                     │
│  R, A, B, C, D, ...                │
└────────────┬───────────────────────┘
             │
             │ conversorMatrizParaDistancias.py
             │
         ┌───┴──────────────────────────┐
         │                              │
         ▼                              ▼
    ┌─────────────────┐      ┌──────────────────┐
    │ .tsp arquivo    │      │ .tsp edges       │
    │ (completo)      │      │ (simplificado)   │
    └─────────────────┘      └────────┬─────────┘
                                       │
                                       │ lerBrasil58.py
                                       │ (carrega distâncias)
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │ Dicionário de distâncias │
                          │ {(i,j): distância, ...}  │
                          └────────┬─────────────────┘
                                   │
                                   │ algoritmoGeneticoBrasil58.py
                                   │ (resolve TSP)
                                   │
                                   ▼
                          ┌──────────────────────────┐
                          │ Melhor Rota Encontrada   │
                          │ Custo Total              │
                          └──────────────────────────┘
```

## 🗂️ Estrutura de Diretórios

```
flyfood_ag_2026_grupo_11/
├── 📄 Arquivos de Documentação
│   ├── README.md                      (original)
│   ├── RESUMO_CONVERSOR.md           (novo) ⭐
│   ├── CONVERSOR_README.md           (novo) ⭐
│   └── GUIA_INTEGRACAO.md            (novo) ⭐
│
├── 🔧 Scripts Python
│   ├── algoritmoGeneticoBrasil58.py   (original)
│   ├── lerBrasil58.py                 (original)
│   ├── conversorMatrizParaDistancias.py (novo) ⭐
│   └── teste_conversor.py             (novo) ⭐
│
├── 📊 Arquivos de Dados (Entrada)
│   ├── exemplo_entrada.txt            (novo) ⭐
│   ├── exemplo_grande.txt             (novo) ⭐
│   ├── brazil58.tsp                   (original)
│   └── edgesbrasil58.tsp              (original)
│
└── 📊 Arquivos de Dados (Saída Gerada)
    ├── exemplo_entrada_distancias.tsp (gerado) ⭐
    └── exemplo_entrada_edges.tsp      (gerado) ⭐
```

## 📋 Formato de Arquivos

### Entrada: Matriz de Pontos

```txt
<linhas> <colunas>
<matriz com '0' para vazio e letras para pontos>
```

**Exemplo:**
```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

### Saída 1: TSP Completo

```txt
NAME: [problema]
TYPE: TSP
DIMENSION: [n_cidades]
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: UPPER_ROW
EDGE_WEIGHT_SECTION
[matriz triangular superior]
```

### Saída 2: EDGES Simplificado

```txt
[apenas a matriz triangular superior]
```

## 🧮 Cálculos Utilizados

### Distância Euclidiana
```
d(p1, p2) = √((y₂ - y₁)² + (x₂ - x₁)²)
```

### Custo Total da Rota
```
Custo = Σ d(cidade[i], cidade[i+1]) + d(cidade[n], cidade[1])
```

## 🎯 Workflow Padrão

1. **Criar entrada:** `minha_entrega.txt` com matriz de pontos
2. **Converter:** `python conversorMatrizParaDistancias.py minha_entrega.txt`
3. **Modificar:** `lerBrasil58.py` para ler arquivo gerado
4. **Ajustar:** Parâmetros em `algoritmoGeneticoBrasil58.py`
5. **Executar:** `python algoritmoGeneticoBrasil58.py`
6. **Analisar:** Resultado e rota encontrada

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Entrada** | Apenas TSP pré-processado | Matriz visual de pontos |
| **Flexibilidade** | Fixa (brasil58) | Qualquer problema |
| **Conversão** | Manual | Automatizada |
| **Documentação** | Mínima | Completa |
| **Integração** | Direta | Via conversor |

## 🚀 Próximos Passos Possíveis

1. **Visualização gráfica:** Plotar matriz e rota final
2. **Interface gráfica:** GUI para criar/visualizar matrizes
3. **Validação de rotas:** Verificar se rota é viável
4. **Exportação:** Salvar rota em diferentes formatos
5. **Comparação:** Comparar múltiplas soluções

## 📞 Resumo de Comandos

```bash
# Converter arquivo
python conversorMatrizParaDistancias.py entrada.txt

# Com nomes customizados
python conversorMatrizParaDistancias.py entrada.txt saida.tsp saida_edges.tsp

# Testar conversor
python teste_conversor.py

# Executar algoritmo genético (após modificar lerBrasil58.py)
python algoritmoGeneticoBrasil58.py
```

## ✅ Checklist de Uso

- [ ] Criar arquivo de entrada `minha_entrega.txt`
- [ ] Executar conversor: `python conversorMatrizParaDistancias.py minha_entrega.txt`
- [ ] Verificar arquivos gerados: `minha_entrega_edges.tsp`
- [ ] Modificar `lerBrasil58.py` para abrir arquivo novo
- [ ] Ajustar `QTDE_CIDADES` em `algoritmoGeneticoBrasil58.py`
- [ ] Executar algoritmo: `python algoritmoGeneticoBrasil58.py`
- [ ] Analisar resultado

---

**Criado:** May 27, 2026  
**Projeto:** FlyFood AG 2026 Grupo 11  
**Status:** ✅ Sistema completo e testado
