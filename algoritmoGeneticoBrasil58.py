import random
from lerBrasil58 import distancias, custoCaminho, inicializaPopulacao, calculaAptidao

# ---------------------------------------------------------------
# Algoritmo Genetico para o problema do Caixeiro Viajante (Brasil58)
#
# Operadores usados:
#   - Selecao de pais: TORNEIO (k=3)
#   - Crossover: ORDER CROSSOVER (OX1)
#   - Mutacao: INVERSION + SCRAMBLE (cada uma com sua propria taxa)
#   - Elitismo: preserva os melhores individuos a cada geracao
# ---------------------------------------------------------------

QTDE_CIDADES      = 58
TAMANHO_POPULACAO = 150
NUM_GERACOES      = 10000
TAXA_CROSSOVER    = 0.9
TAXA_MUT_INVERSAO = 0.2
TAXA_MUT_SCRAMBLE = 0.05
TAMANHO_TORNEIO   = 3
TAMANHO_ELITE     = 2


# ---------------------------------------------------------------
# 1) SELECAO DE PAIS - Torneio
#    Sorteia k individuos e devolve o de menor custo (melhor).
# ---------------------------------------------------------------
def selecaoTorneio(populacao, aptidoes, k):
    indices = random.sample(range(len(populacao)), k)
    melhor = indices[0]
    for idx in indices[1:]:
        if aptidoes[idx] < aptidoes[melhor]:
            melhor = idx
    return populacao[melhor]


# ---------------------------------------------------------------
# 2) CROSSOVER - Order Crossover (OX1)
#    - Copia um trecho [a..b] do pai1 para o filho.
#    - Completa o restante na ordem em que aparecem no pai2,
#      pulando genes ja presentes no trecho copiado.
# ---------------------------------------------------------------
def orderCrossover(pai1, pai2):
    n = len(pai1)
    a, b = sorted(random.sample(range(n), 2))

    filho = [None] * n
    filho[a:b+1] = pai1[a:b+1]
    fixos = set(filho[a:b+1])

    # genes do pai2 a partir do ponto b+1, em ordem circular
    sequenciaPai2 = pai2[b+1:] + pai2[:b+1]
    resto = [g for g in sequenciaPai2 if g not in fixos]

    idx = (b + 1) % n
    for gene in resto:
        filho[idx] = gene
        idx = (idx + 1) % n
    return filho


# ---------------------------------------------------------------
# 3) MUTACAO - Inversion
#    Inverte a ordem de um trecho aleatorio.
#    Eficaz em TSP pois preserva varias arestas adjacentes.
# ---------------------------------------------------------------
def mutacaoInversion(individuo):
    a, b = sorted(random.sample(range(len(individuo)), 2))
    individuo[a:b+1] = reversed(individuo[a:b+1])
    return individuo


# ---------------------------------------------------------------
# 4) MUTACAO - Scramble
#    Embaralha aleatoriamente um trecho. Mais disruptiva que a
#    inversion, ajuda a escapar de otimos locais.
# ---------------------------------------------------------------
def mutacaoScramble(individuo):
    a, b = sorted(random.sample(range(len(individuo)), 2))
    trecho = individuo[a:b+1]
    random.shuffle(trecho)
    individuo[a:b+1] = trecho
    return individuo


# ---------------------------------------------------------------
# 5) Aplica as mutacoes de acordo com as taxas configuradas.
# ---------------------------------------------------------------
def aplicaMutacoes(individuo):
    if random.random() < TAXA_MUT_INVERSAO:
        individuo = mutacaoInversion(individuo)
    if random.random() < TAXA_MUT_SCRAMBLE:
        individuo = mutacaoScramble(individuo)
    return individuo


# ---------------------------------------------------------------
# 6) SELECAO DE SOBREVIVENTES - Steady State com Torneio
#    Mescla filhos com a população e seleciona os melhores
#    para permanecer na população via torneio.
# ---------------------------------------------------------------
def selecaoSobreviventes(populacao, aptidoes, filhos, tamanho_torneio=3):
    """
    Seleciona sobreviventes usando modelo Steady State.
    
    Processo:
    1. Mescla filhos com população atual
    2. Usa torneio para selecionar os melhores
    3. Mantém tamanho original da população
    
    Args:
        populacao: lista de indivíduos
        aptidoes: lista de aptidões (custos) dos indivíduos
        filhos: lista de novos indivíduos (filhos gerados)
        tamanho_torneio: k para seleção por torneio
        
    Returns:
        tuple: (população_selecionada, aptidoes_selecionadas)
    """
    # Calcula aptidões dos filhos
    aptidoes_filhos = [custoCaminho(filho, distancias) for filho in filhos]
    
    # Mescla população atual com filhos
    populacao_mesclada = populacao + filhos
    aptidoes_mescladas = aptidoes + aptidoes_filhos
    
    # Reduz ao tamanho original usando seleção por torneio
    tamanho_original = len(populacao)
    populacao_nova = []
    aptidoes_nova = []
    
    # Seleciona indivíduos via torneio até voltar ao tamanho original
    indices_disponiveis = list(range(len(populacao_mesclada)))
    
    for _ in range(tamanho_original):
        # Seleciona k indivíduos aleatórios
        indices_torneio = random.sample(indices_disponiveis, 
                                       min(tamanho_torneio, len(indices_disponiveis)))
        
        # Encontra o melhor entre os selecionados
        melhor_idx = indices_torneio[0]
        for idx in indices_torneio[1:]:
            if aptidoes_mescladas[idx] < aptidoes_mescladas[melhor_idx]:
                melhor_idx = idx
        
        # Adiciona o melhor à nova população
        populacao_nova.append(populacao_mesclada[melhor_idx][:])
        aptidoes_nova.append(aptidoes_mescladas[melhor_idx])
        
        # Remove do pool de disponíveis (sem repetição)
        indices_disponiveis.remove(melhor_idx)
    
    return populacao_nova, aptidoes_nova


# ---------------------------------------------------------------
# 7) LOOP PRINCIPAL DO GA - VERSÃO GERACIONAL (ORIGINAL)
# ---------------------------------------------------------------
def algoritmoGenetico():
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)
    aptidoes  = calculaAptidao(populacao, distancias)

    melhorCustoGlobal = min(aptidoes)
    melhorIndividuo   = populacao[aptidoes.index(melhorCustoGlobal)][:]

    for geracao in range(NUM_GERACOES):
        # ordena populacao por aptidao (menor custo primeiro) para o elitismo
        ordenados = sorted(zip(populacao, aptidoes), key=lambda x: x[1])
        novaPopulacao = [ind[:] for ind, _ in ordenados[:TAMANHO_ELITE]]

        # preenche o resto da nova populacao
        while len(novaPopulacao) < TAMANHO_POPULACAO:
            pai1 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)
            pai2 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)

            if random.random() < TAXA_CROSSOVER:
                filho1 = orderCrossover(pai1, pai2)
                filho2 = orderCrossover(pai2, pai1)
            else:
                filho1, filho2 = pai1[:], pai2[:]

            filho1 = aplicaMutacoes(filho1)
            filho2 = aplicaMutacoes(filho2)

            novaPopulacao.append(filho1)
            if len(novaPopulacao) < TAMANHO_POPULACAO:
                novaPopulacao.append(filho2)

        populacao = novaPopulacao
        aptidoes  = calculaAptidao(populacao, distancias)

        melhorAtual = min(aptidoes)
        if melhorAtual < melhorCustoGlobal:
            melhorCustoGlobal = melhorAtual
            melhorIndividuo   = populacao[aptidoes.index(melhorAtual)][:]

        if geracao % 50 == 0 or geracao == NUM_GERACOES - 1:
            print(f"Geracao {geracao:4d} | melhor atual: {melhorAtual} | melhor global: {melhorCustoGlobal}")

    return melhorIndividuo, melhorCustoGlobal


# ---------------------------------------------------------------
# 8) LOOP PRINCIPAL DO GA - VERSÃO STEADY STATE
#    Filhos são inseridos incrementalmente e competem com a 
#    população via seleção de torneio para sobreviver.
# ---------------------------------------------------------------
def algoritmoGeneticoSteadyState():
    """
    Algoritmo Genético com modelo Steady State (Estado Estacionário).
    
    Diferenças em relação ao modelo geracional:
    - Filhos são inseridos continuamente na população
    - Usa seleção de torneio para escolher quem sobrevive
    - Melhor convergência em problemas de otimização discreta
    """
    populacao = inicializaPopulacao(TAMANHO_POPULACAO, QTDE_CIDADES)
    aptidoes  = calculaAptidao(populacao, distancias)

    melhorCustoGlobal = min(aptidoes)
    melhorIndividuo   = populacao[aptidoes.index(melhorCustoGlobal)][:]

    # Contador de avaliações de fitness
    num_avaliacoes = TAMANHO_POPULACAO

    for geracao in range(NUM_GERACOES):
        filhos = []
        
        # Gera filhos (proporcionalmente ao tamanho da população)
        num_filhos = TAMANHO_POPULACAO // 2
        
        for _ in range(num_filhos):
            pai1 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)
            pai2 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)

            if random.random() < TAXA_CROSSOVER:
                filho1 = orderCrossover(pai1[:], pai2[:])
                filho2 = orderCrossover(pai2[:], pai1[:])
            else:
                filho1, filho2 = pai1[:], pai2[:]

            filho1 = aplicaMutacoes(filho1)
            filho2 = aplicaMutacoes(filho2)

            filhos.append(filho1)
            if len(filhos) < num_filhos:
                filhos.append(filho2)
        
        # ===== SELECAO DE SOBREVIVENTES (STEADY STATE) =====
        # Mescla filhos com população e seleciona os melhores
        populacao, aptidoes = selecaoSobreviventes(populacao, aptidoes, filhos, 
                                                    tamanho_torneio=TAMANHO_TORNEIO)
        
        # Atualiza melhor encontrado globalmente
        melhorAtual = min(aptidoes)
        if melhorAtual < melhorCustoGlobal:
            melhorCustoGlobal = melhorAtual
            melhorIndividuo   = populacao[aptidoes.index(melhorAtual)][:]

        # Atualiza contador
        num_avaliacoes += len(filhos)

        if geracao % 50 == 0 or geracao == NUM_GERACOES - 1:
            print(f"Geracao {geracao:4d} | melhor atual: {melhorAtual:6d} | "
                  f"melhor global: {melhorCustoGlobal:6d} | "
                  f"avaliacoes: {num_avaliacoes}")

    return melhorIndividuo, melhorCustoGlobal


# ---------------------------------------------------------------
# 9) VERSÃO COM AMBOS OS MODELOS - COMPARAÇÃO
# ---------------------------------------------------------------
def algoritmoGeneticoHibrido():
    """
    Versão híbrida que permite comparar ambos os modelos.
    Use a função desejada abaixo.
    """
    print("\n" + "="*70)
    print("COMPARAÇÃO DE MODELOS")
    print("="*70)
    
    print("\n--- Modelo GERACIONAL (Original) ---")
    rota_ger, custo_ger = algoritmoGenetico()
    
    print("\n--- Modelo STEADY STATE ---")
    rota_ss, custo_ss = algoritmoGeneticoSteadyState()
    
    print("\n" + "="*70)
    print("RESULTADO FINAL")
    print("="*70)
    print(f"\nModelo Geracional:")
    print(f"  Custo: {custo_ger}")
    print(f"  Rota:  {rota_ger}")
    
    print(f"\nModelo Steady State:")
    print(f"  Custo: {custo_ss}")
    print(f"  Rota:  {rota_ss}")
    
    print(f"\nDiferença: {custo_ger - custo_ss:+d}")
    print("="*70)


if __name__ == "__main__":
    random.seed()  # remova o seed ou fixe para reproduzir
    
    # ===== ESCOLHA QUAL MODELO USAR =====
    
    # Opção 1: Modelo Geracional (Original)
    #print("\n[1/3] Executando Algoritmo Genético - MODELO GERACIONAL")
    #melhorRota, melhorCusto = algoritmoGenetico()
    
    # Opção 2: Modelo Steady State
    # print("\n[1/2] Executando Algoritmo Genético - MODELO STEADY STATE")
    # melhorRota, melhorCusto = algoritmoGeneticoSteadyState()
    
    # Opção 3: Comparar ambos os modelos
    algoritmoGeneticoHibrido()
    melhorRota = None  # Para não imprimir resultado duplicado
    
    if melhorRota is not None:
        print("\n=== Resultado final ===")
        print(f"Custo: {melhorCusto}")
        print(f"Rota:  {melhorRota}")
