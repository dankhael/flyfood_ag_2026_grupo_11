"""
Algoritmo Genético para TSP - Versão Flexível

Funciona com qualquer número de cidades.
Usa a versão flexível de lerBrasil58 que detecta automaticamente o número de cidades.

Operadores:
  - Seleção: TORNEIO (k=3)
  - Crossover: ORDER CROSSOVER (OX1)
  - Mutação: INVERSION + SCRAMBLE
  - Elitismo: preserva os melhores indivíduos
"""

import random
from lerBrasil58_Flexivel import ler_arquivo_distancias, custoCaminho, inicializaPopulacao, calculaAptidao

# ---------------------------------------------------------------
# PARAMETROS DO ALGORITMO
# Estes podem ser ajustados conforme necessário
# ---------------------------------------------------------------
TAMANHO_POPULACAO = 50      # Reduzido para problemas menores
NUM_GERACOES      = 200     # Reduzido para testes rápidos
TAXA_CROSSOVER    = 0.9
TAXA_MUT_INVERSAO = 0.2
TAXA_MUT_SCRAMBLE = 0.05
TAMANHO_TORNEIO   = 3
TAMANHO_ELITE     = 2

# Arquivo de entrada (pode ser alterado)
ARQUIVO_DISTANCIAS = "exemplo_entrada_edges.tsp"


# ---------------------------------------------------------------
# 1) SELECAO DE PAIS - Torneio
# ---------------------------------------------------------------
def selecaoTorneio(populacao, aptidoes, k):
    """Seleciona k indivíduos aleatoriamente e retorna o melhor."""
    indices = random.sample(range(len(populacao)), k)
    melhor = indices[0]
    for idx in indices[1:]:
        if aptidoes[idx] < aptidoes[melhor]:
            melhor = idx
    return populacao[melhor]


# ---------------------------------------------------------------
# 2) CROSSOVER - Order Crossover (OX1)
# ---------------------------------------------------------------
def orderCrossover(pai1, pai2):
    """Executa Order Crossover (OX1) entre dois pais."""
    n = len(pai1)
    a, b = sorted(random.sample(range(n), 2))

    filho = [None] * n
    filho[a:b+1] = pai1[a:b+1]
    fixos = set(filho[a:b+1])

    # Genes do pai2 a partir do ponto b+1, em ordem circular
    sequenciaPai2 = pai2[b+1:] + pai2[:b+1]
    resto = [g for g in sequenciaPai2 if g not in fixos]

    idx = (b + 1) % n
    for gene in resto:
        filho[idx] = gene
        idx = (idx + 1) % n
    return filho


# ---------------------------------------------------------------
# 3) MUTACAO - Inversion
# ---------------------------------------------------------------
def mutacaoInversion(individuo):
    """Inverte um trecho aleatório do indivíduo."""
    a, b = sorted(random.sample(range(len(individuo)), 2))
    individuo[a:b+1] = reversed(individuo[a:b+1])
    return individuo


# ---------------------------------------------------------------
# 4) MUTACAO - Scramble
# ---------------------------------------------------------------
def mutacaoScramble(individuo):
    """Embaralha um trecho aleatório do indivíduo."""
    a, b = sorted(random.sample(range(len(individuo)), 2))
    trecho = individuo[a:b+1]
    random.shuffle(trecho)
    individuo[a:b+1] = trecho
    return individuo


# ---------------------------------------------------------------
# 5) Aplica as mutacoes
# ---------------------------------------------------------------
def aplicaMutacoes(individuo):
    """Aplica mutações de acordo com as taxas configuradas."""
    if random.random() < TAXA_MUT_INVERSAO:
        individuo = mutacaoInversion(individuo[:])
    if random.random() < TAXA_MUT_SCRAMBLE:
        individuo = mutacaoScramble(individuo[:])
    return individuo


# ---------------------------------------------------------------
# 6) ALGORITMO GENÉTICO
# ---------------------------------------------------------------
def algoritmoGeneticoFlexivel(arquivo_distancias=ARQUIVO_DISTANCIAS,
                              tamanho_populacao=None,
                              num_geracoes=None):
    """
    Executa o algoritmo genético para resolver o TSP.
    
    Args:
        arquivo_distancias: caminho do arquivo com distâncias
        tamanho_populacao: tamanho da população (None = usar padrão)
        num_geracoes: número de gerações (None = usar padrão)
        
    Returns:
        tuple: (melhor_rota, melhor_custo, num_cidades)
    """
    
    # Usa valores padrão se não informados
    if tamanho_populacao is None:
        tamanho_populacao = TAMANHO_POPULACAO
    if num_geracoes is None:
        num_geracoes = NUM_GERACOES
    
    print("\n" + "=" * 70)
    print("ALGORITMO GENÉTICO PARA TSP - VERSÃO FLEXÍVEL")
    print("=" * 70)
    
    # -------------------------------------------------------
    # PASSO 1: Carregar distâncias
    # -------------------------------------------------------
    print(f"\n1. Carregando arquivo: {arquivo_distancias}")
    distancias, num_cidades = ler_arquivo_distancias(arquivo_distancias)
    
    if not distancias or num_cidades == 0:
        print("✗ Erro ao carregar arquivo!")
        return None, None, 0
    
    print(f"   ✓ Carregado com sucesso!")
    print(f"   Número de cidades: {num_cidades}")
    
    # -------------------------------------------------------
    # PASSO 2: Inicializar população
    # -------------------------------------------------------
    print(f"\n2. Inicializando população...")
    print(f"   Tamanho da população: {tamanho_populacao}")
    print(f"   Número de gerações: {num_geracoes}")
    
    populacao = inicializaPopulacao(tamanho_populacao, num_cidades)
    aptidoes = calculaAptidao(populacao, distancias)
    
    melhorCustoGlobal = min(aptidoes)
    melhorIndividuo = populacao[aptidoes.index(melhorCustoGlobal)][:]
    
    print(f"   ✓ População inicializada")
    print(f"   Melhor custo inicial: {melhorCustoGlobal}")
    
    # -------------------------------------------------------
    # PASSO 3: Evolução
    # -------------------------------------------------------
    print(f"\n3. Evoluindo população...")
    print("-" * 70)
    
    for geracao in range(num_geracoes):
        # Ordena população por aptidão (elitismo)
        ordenados = sorted(zip(populacao, aptidoes), key=lambda x: x[1])
        novaPopulacao = [ind[:] for ind, _ in ordenados[:TAMANHO_ELITE]]
        
        # Preenche resto da população
        while len(novaPopulacao) < tamanho_populacao:
            pai1 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)
            pai2 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)
            
            if random.random() < TAXA_CROSSOVER:
                filho1 = orderCrossover(pai1[:], pai2[:])
                filho2 = orderCrossover(pai2[:], pai1[:])
            else:
                filho1, filho2 = pai1[:], pai2[:]
            
            filho1 = aplicaMutacoes(filho1)
            filho2 = aplicaMutacoes(filho2)
            
            novaPopulacao.append(filho1)
            if len(novaPopulacao) < tamanho_populacao:
                novaPopulacao.append(filho2)
        
        populacao = novaPopulacao
        aptidoes = calculaAptidao(populacao, distancias)
        
        melhorAtual = min(aptidoes)
        if melhorAtual < melhorCustoGlobal:
            melhorCustoGlobal = melhorAtual
            melhorIndividuo = populacao[aptidoes.index(melhorAtual)][:]
        
        # Exibe progresso a cada 20 gerações ou na última
        if geracao % max(1, num_geracoes // 10) == 0 or geracao == num_geracoes - 1:
            print(f"Geração {geracao:4d} | Melhor atual: {melhorAtual:6d} | Melhor global: {melhorCustoGlobal:6d}")
    
    print("-" * 70)
    
    return melhorIndividuo, melhorCustoGlobal, num_cidades


# ---------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Configura seed para reproduzibilidade (remova para resultados aleatórios)
    random.seed()
    
    # Executa o algoritmo
    melhorRota, melhorCusto, num_cidades = algoritmoGeneticoFlexivel()
    
    if melhorRota is not None:
        print("\n" + "=" * 70)
        print("RESULTADO FINAL")
        print("=" * 70)
        print(f"Número de cidades: {num_cidades}")
        print(f"Custo total: {melhorCusto}")
        print(f"Rota: {melhorRota}")
        print(f"\nInterpretação da rota:")
        print(f"  Índice 1 = Origem (R)")
        print(f"  Índices 2+ = Pontos de entrega (A, B, C, ...)")
        print("=" * 70 + "\n")
    else:
        print("\n✗ Erro ao executar o algoritmo genético!")
