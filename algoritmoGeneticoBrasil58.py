import random
from lerBrasil58 import distancias, qtdeCidades, inicializaPopulacao, calculaAptidao

# ---------------------------------------------------------------
# Algoritmo Genetico para o problema do Caixeiro Viajante (Brasil58)
#
# Operadores usados:
#   - Selecao de pais: TORNEIO (k=5)
#   - Crossover: ORDER CROSSOVER (OX1)
#   - Mutacao: INVERSION + SCRAMBLE (cada uma com sua propria taxa)
#   - Selecao de sobreviventes: STEADY-STATE com eliminacao de duplicatas
#     (mescla pais + filhos, descarta clones e mantem os melhores; o
#     melhor individuo nunca e perdido e a diversidade e preservada)
# ---------------------------------------------------------------

QTDE_CIDADES      = qtdeCidades
TAMANHO_POPULACAO = 200
NUM_GERACOES      = 5000
TAXA_CROSSOVER    = 0.9
TAXA_MUT_INVERSAO = 0.5
TAXA_MUT_SCRAMBLE = 0.10
TAMANHO_TORNEIO   = 5
NUM_FILHOS        = 100    # quantos filhos gerar por geracao (lambda)


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
# 6) SELECAO DE SOBREVIVENTES - Steady-state (mu + lambda)
#    Em vez do esquema "geracional" (em que os filhos substituem
#    totalmente a populacao anterior), mesclamos pais + filhos em um
#    unico conjunto e selecionamos os melhores como sobreviventes.
#    Assim o melhor individuo nunca e perdido (elitismo implicito),
#    conforme o lembrete do quadro: "salvar o melhor individuo".
#
#    ELIMINACAO DE DUPLICATAS: o steady-state elitista tende a encher
#    a populacao de copias do melhor individuo, o que mata a diversidade
#    e trava a busca cedo (convergencia prematura). Por isso priorizamos
#    individuos UNICOS; rotas repetidas so entram para completar a
#    populacao se nao houver unicos suficientes. Isso mantem a busca
#    produtiva por muito mais geracoes e aproxima o resultado do otimo.
# ---------------------------------------------------------------
def selecaoSobreviventes(populacao, aptidoes, filhos, aptidoesFilhos, tamanho):
    # mescla o conjunto de pais com o de filhos, cada um com sua aptidao
    combinados = list(zip(populacao, aptidoes)) + list(zip(filhos, aptidoesFilhos))
    # ordena por custo (menor primeiro)
    combinados.sort(key=lambda x: x[1])

    # separa individuos unicos (1a ocorrencia) das duplicatas
    vistos = set()
    unicos, duplicatas = [], []
    for ind, apt in combinados:
        chave = tuple(ind)
        if chave in vistos:
            duplicatas.append((ind, apt))
        else:
            vistos.add(chave)
            unicos.append((ind, apt))

    # preenche com unicos; se faltar, completa com as melhores duplicatas
    escolhidos = (unicos + duplicatas)[:tamanho]
    sobreviventes  = [ind for ind, _ in escolhidos]
    aptidoesSobrev = [apt for _, apt in escolhidos]
    return sobreviventes, aptidoesSobrev


# ---------------------------------------------------------------
# 7) LOOP PRINCIPAL DO GA
#    Os parametros sao opcionais: quando omitidos, usam os valores
#    configurados no topo do modulo (instancia Brasil58). Informando-os
#    e possivel rodar o GA sobre QUALQUER problema (ex.: uma grade do
#    FLYFOOD convertida), o que tambem facilita os testes automatizados.
#    'verbose' liga/desliga o log de progresso e 'intervaloLog' controla
#    de quantas em quantas geracoes ele e impresso.
# ---------------------------------------------------------------
def algoritmoGenetico(dicDistancias=None, qtdeCidades=None, numGeracoes=None,
                      tamanhoPopulacao=None, numFilhos=None,
                      verbose=True, intervaloLog=50):
    if dicDistancias    is None: dicDistancias    = distancias
    if qtdeCidades      is None: qtdeCidades      = QTDE_CIDADES
    if numGeracoes      is None: numGeracoes      = NUM_GERACOES
    if tamanhoPopulacao is None: tamanhoPopulacao = TAMANHO_POPULACAO
    if numFilhos        is None: numFilhos        = NUM_FILHOS

    populacao = inicializaPopulacao(tamanhoPopulacao, qtdeCidades)
    aptidoes  = calculaAptidao(populacao, dicDistancias)

    melhorCustoGlobal = min(aptidoes)
    melhorIndividuo   = populacao[aptidoes.index(melhorCustoGlobal)][:]

    for geracao in range(numGeracoes):
        # gera os filhos (descendentes) a partir da populacao atual (pais)
        filhos = []
        while len(filhos) < numFilhos:
            pai1 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)
            pai2 = selecaoTorneio(populacao, aptidoes, TAMANHO_TORNEIO)

            if random.random() < TAXA_CROSSOVER:
                filho1 = orderCrossover(pai1, pai2)
                filho2 = orderCrossover(pai2, pai1)
            else:
                filho1, filho2 = pai1[:], pai2[:]

            filho1 = aplicaMutacoes(filho1)
            filho2 = aplicaMutacoes(filho2)

            filhos.append(filho1)
            if len(filhos) < numFilhos:
                filhos.append(filho2)

        aptidoesFilhos = calculaAptidao(filhos, dicDistancias)

        # STEADY-STATE: mescla pais + filhos e seleciona os sobreviventes
        populacao, aptidoes = selecaoSobreviventes(
            populacao, aptidoes, filhos, aptidoesFilhos, tamanhoPopulacao
        )

        # a selecao de sobreviventes ja devolve a populacao ordenada,
        # entao o melhor da geracao esta na posicao 0
        melhorAtual = aptidoes[0]
        if melhorAtual < melhorCustoGlobal:
            melhorCustoGlobal = melhorAtual
            melhorIndividuo   = populacao[0][:]

        if verbose and (geracao % intervaloLog == 0 or geracao == numGeracoes - 1):
            print(f"Geracao {geracao:4d} | melhor atual: {melhorAtual} | melhor global: {melhorCustoGlobal}")

    return melhorIndividuo, melhorCustoGlobal


if __name__ == "__main__":
    random.seed()  # remova o seed ou fixe para reproduzir
    melhorRota, melhorCusto = algoritmoGenetico()
    print("\n=== Resultado final ===")
    print(f"Custo: {melhorCusto}")
    print(f"Rota:  {melhorRota}")
