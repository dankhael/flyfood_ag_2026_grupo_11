# 🚁 Sistema de Conversão de Matriz para Distâncias TSP

## Resumo do que foi criado

Você agora possui um **sistema completo** para converter matrizes de pontos de entrega para o formato de distâncias TSP, pronto para ser usado com o algoritmo genético.

### Arquivos Criados

```
📁 /workspaces/flyfood_ag_2026_grupo_11/
│
├── 🔧 conversorMatrizParaDistancias.py    ← SCRIPT PRINCIPAL
│   └── Converte matriz de pontos → distâncias
│
├── 📄 teste_conversor.py                  ← TESTES
│   └── Valida o funcionamento do conversor
│
├── 📋 exemplo_entrada.txt                 ← EXEMPLO 1 (simples)
│   ├── exemplo_entrada_distancias.tsp     (gerado automaticamente)
│   └── exemplo_entrada_edges.tsp          (gerado automaticamente)
│
├── 📋 exemplo_grande.txt                  ← EXEMPLO 2 (complexo)
│
├── 📚 CONVERSOR_README.md                 ← DOCUMENTAÇÃO COMPLETA
├── 📚 GUIA_INTEGRACAO.md                  ← GUIA DE USO COM AG
└── 📚 ARQUIVOS_ORIGINAIS.md               ← REFERÊNCIA

ARQUIVOS ORIGINAIS (intactos):
├── algoritmoGeneticoBrasil58.py
├── lerBrasil58.py
├── brazil58.tsp
├── edgesbrasil58.tsp
└── README.md
```

## 🚀 Início Rápido (3 passos)

### 1️⃣ Criar arquivo de entrada

Crie um arquivo `minha_entrega.txt`:

```txt
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

**Regras:**
- Primeira linha: `<linhas> <colunas>`
- `R` = origem (apenas um)
- `A-Z` = pontos de entrega
- `0` = vazio

### 2️⃣ Executar conversor

```bash
python conversorMatrizParaDistancias.py minha_entrega.txt
```

**Gera:**
- `minha_entrega_distancias.tsp` (formato TSP completo)
- `minha_entrega_edges.tsp` (matriz de distâncias simplificada)

### 3️⃣ Usar com algoritmo genético

Modifique `lerBrasil58.py`:

```python
# Altere esta linha:
objArq = open("edgesbrasil58.tsp")

# Para:
objArq = open("minha_entrega_edges.tsp")
```

Ajuste `algoritmoGeneticoBrasil58.py`:

```python
QTDE_CIDADES = 5  # número total de pontos (R + A + B + C + D)
```

Execute:

```bash
python algoritmoGeneticoBrasil58.py
```

## 📖 Documentação

| Arquivo | Descrição |
|---------|-----------|
| **CONVERSOR_README.md** | Documentação completa do conversor |
| **GUIA_INTEGRACAO.md** | Como usar com o algoritmo genético |
| **exemplo_entrada.txt** | Exemplo simples para testar |
| **exemplo_grande.txt** | Exemplo com mais pontos |

## 🔍 Exemplos

### Exemplo 1: Matriz Simples

**Entrada:** `exemplo_entrada.txt`
```
4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0
```

**Saída:** Matriz de distâncias 5x5 (R, A, B, C, D)

```
2 2 4 5    (distâncias de R para A, B, C, D)
2 3 3      (distâncias de A para B, C, D)
2 4        (distâncias de B para C, D)
2          (distância de C para D)
```

### Exemplo 2: Matriz Grande

Veja `exemplo_grande.txt` para um exemplo com 10 pontos de entrega.

## ⚙️ Como Funciona

```
Matriz 4x5               Coordenadas          Distâncias Euclidianas
┌─────────────┐         ┌──────────────┐     ┌──────────────────┐
│ 0 0 0 0 D │          │ R: (3,0)     │     │ R-A: 2           │
│ 0 A 0 0 0 │    →      │ A: (1,1)     │  →  │ R-B: 2           │
│ 0 0 0 0 C │          │ B: (3,2)     │     │ R-C: 4           │
│ R 0 B 0 0 │          │ C: (2,4)     │     │ R-D: 5           │
└─────────────┘         │ D: (0,4)     │     │ etc...           │
                        └──────────────┘     └──────────────────┘
```

1. **Leitura**: Extrai coordenadas (linha, coluna) de cada ponto
2. **Cálculo**: Usa distância euclidiana: d = √((y₂-y₁)² + (x₂-x₁)²)
3. **Ordenação**: R primeiro, depois A, B, C, ... (alfabético)
4. **Saída**: Matriz triangular superior de distâncias

## ✅ Validações Realizadas

- ✓ Arquivo existe e é legível
- ✓ Dimensões da matriz são consistentes
- ✓ Existe exatamente um ponto de origem `R`
- ✓ Nenhum ponto duplicado
- ✓ Distâncias calculadas corretamente

## 🎯 Casos de Uso

- **Roteamento de Drones**: Otimize entregas com drone
- **TSP**: Problema do Caixeiro Viajante genérico
- **Logística**: Otimize rotas de entrega
- **Pesquisa**: Teste algoritmos de otimização

## 💡 Dicas

1. **Comece pequeno**: Use exemplo_entrada.txt primeiro
2. **Valide visualmente**: Confirme se as coordenadas fazem sentido
3. **Ajuste parâmetros**: Tamanho populacional e gerações
4. **Documente**: Salve configurações que funcionaram bem
5. **Compare**: Compare resultados com diferentes parâmetros

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| Arquivo não encontrado | Verifique caminho e nome |
| Erro de dimensão | Conta linhas/colunas corretamente |
| Sem ponto R | Adicione um `R` na matriz |
| Distâncias erradas | Verifique coordenadas dos pontos |

## 📞 Suporte

Para mais informações, consulte:
- `CONVERSOR_README.md` - Documentação técnica
- `GUIA_INTEGRACAO.md` - Integração com AG
- `conversorMatrizParaDistancias.py` - Código-fonte comentado

---

**Desenvolvido para:** Otimização de Rotas com Algoritmo Genético  
**Formato de entrada:** Matriz com pontos marcados  
**Formato de saída:** TSP (UPPER_ROW) / EDGES  
**Compatível com:** `lerBrasil58.py` e `algoritmoGeneticoBrasil58.py`
