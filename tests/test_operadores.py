"""Testes de unidade dos operadores do Algoritmo Genetico.

Verificam as propriedades fundamentais de cada operador. A mais importante
em TSP e: todo operador deve devolver uma PERMUTACAO valida (cada cidade
aparece exatamente uma vez) -- caso contrario a rota seria invalida.
"""

import logging
import random

import algoritmoGeneticoBrasil58 as ag

log = logging.getLogger(__name__)


def ehPermutacao(rota, n):
    """True se 'rota' contem cada cidade de 1..n exatamente uma vez."""
    return sorted(rota) == list(range(1, n + 1))


def test_order_crossover_gera_permutacao_valida():
    random.seed(0)
    n = 10
    pai1 = list(range(1, n + 1)); random.shuffle(pai1)
    pai2 = list(range(1, n + 1)); random.shuffle(pai2)

    filho = ag.orderCrossover(pai1, pai2)

    assert ehPermutacao(filho, n), "OX1 deve preservar a permutacao"
    log.info("OX1: filho=%s e permutacao valida de 1..%d", filho, n)


def test_mutacao_inversion_preserva_permutacao():
    random.seed(1)
    individuo = list(range(1, 11))
    ag.mutacaoInversion(individuo)
    assert ehPermutacao(individuo, 10)


def test_mutacao_scramble_preserva_permutacao():
    random.seed(2)
    individuo = list(range(1, 11))
    ag.mutacaoScramble(individuo)
    assert ehPermutacao(individuo, 10)


def test_torneio_seleciona_o_de_menor_custo():
    # com k = tamanho da populacao, o torneio sempre devolve o melhor
    populacao = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    aptidoes = [30, 10, 20]
    random.seed(0)

    vencedor = ag.selecaoTorneio(populacao, aptidoes, k=3)

    assert vencedor == [4, 5, 6], "deve vencer o individuo de menor custo (10)"


def test_steady_state_preserva_o_melhor():
    # o melhor (menor custo) deve estar sempre na posicao 0 dos sobreviventes
    pais = [[1, 2, 3], [3, 2, 1]]
    aptPais = [100, 90]
    filhos = [[2, 1, 3], [1, 3, 2]]
    aptFilhos = [40, 70]

    sobrev, aptSobrev = ag.selecaoSobreviventes(pais, aptPais, filhos, aptFilhos, tamanho=2)

    assert aptSobrev == sorted(aptSobrev), "sobreviventes saem ordenados por custo"
    assert aptSobrev[0] == 40, "o melhor individuo nunca e perdido"
    log.info("Steady-state: melhor custo preservado = %d", aptSobrev[0])


def test_steady_state_elimina_duplicatas():
    # populacao tomada por clones do melhor; a dedup deve garantir diversidade
    pais = [[1, 2, 3], [1, 2, 3]]   # mesmos genes (duplicatas)
    aptPais = [10, 10]
    filhos = [[3, 2, 1]]
    aptFilhos = [20]

    sobrev, aptSobrev = ag.selecaoSobreviventes(pais, aptPais, filhos, aptFilhos, tamanho=2)

    assert aptSobrev[0] == 10, "o melhor ainda sobrevive"
    assert tuple(sobrev[0]) != tuple(sobrev[1]), "nao deve haver clones se ha unicos"
    log.info("Steady-state: duplicata eliminada -> sobreviventes unicos %s", sobrev)
