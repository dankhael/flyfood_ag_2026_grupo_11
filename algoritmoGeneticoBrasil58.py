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
NUM_GERACOES      = 1000
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
# 6) LOOP PRINCIPAL DO GA
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


if __name__ == "__main__":
    random.seed()  # remova o seed ou fixe para reproduzir
    melhorRota, melhorCusto = algoritmoGenetico()
    print("\n=== Resultado final ===")
    print(f"Custo: {melhorCusto}")
    print(f"Rota:  {melhorRota}")
