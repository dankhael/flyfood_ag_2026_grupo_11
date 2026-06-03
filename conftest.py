"""Configuracao compartilhada dos testes (pytest).

Este arquivo e carregado automaticamente pelo pytest ANTES dos testes.
Ele garante que:
  1. os modulos do projeto sejam importaveis de qualquer lugar;
  2. os arquivos de dados (ex.: edgesbrasil58.tsp) sejam encontrados,
     pois sao abertos por caminho relativo.

Tambem oferece "fixtures" (ajudantes reutilizaveis pelos testes):
  - forca_bruta:     resolve o TSP de forma exata (so para instancias pequenas);
  - converte_grade:  faz o pipeline grade-de-texto -> matriz de distancias.
"""

import itertools
import os
import sys

import pytest

# --- 1) torna o projeto importavel e fixa o diretorio de trabalho ---
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

from lerBrasil58 import custoCaminho, lerDistancias  # noqa: E402
import conversorMatrizParaDistancias as conv          # noqa: E402


def forcaBruta(qtdeCidades, dicDistancias):
    """Resolve o TSP testando TODAS as rotas possiveis (forca bruta).

    Fixa a primeira cidade para nao recontar rotas equivalentes por rotacao.
    So e viavel para instancias pequenas (poucas cidades) -- exatamente o
    caso das grades usadas nos testes. Devolve o custo OTIMO, que serve de
    gabarito para comparar com a resposta do Algoritmo Genetico.
    """
    cidades = list(range(1, qtdeCidades + 1))
    base, resto = cidades[0], cidades[1:]
    melhor = None
    for perm in itertools.permutations(resto):
        custo = custoCaminho([base] + list(perm), dicDistancias)
        if melhor is None or custo < melhor:
            melhor = custo
    return melhor


@pytest.fixture
def forca_bruta():
    """Disponibiliza a funcao de forca bruta para os testes."""
    return forcaBruta


@pytest.fixture
def converte_grade(tmp_path):
    """Fabrica que converte uma grade de texto em um problema de TSP.

    Recebe o texto da grade (formato do FLYFOOD), grava em arquivo, roda o
    conversor para a matriz triangular de distancias e a le de volta.
    Devolve (distancias, qtdeCidades, pontos) prontos para o GA resolver.
    """
    def _converte(textoGrade, nome="grade"):
        entrada = tmp_path / f"{nome}.txt"
        saida = tmp_path / f"{nome}.tsp"
        entrada.write_text(textoGrade)

        pontos = conv.lerPontos(str(entrada))
        matriz = conv.gerarMatriz(pontos)
        conv.salvar(str(saida), matriz)

        distancias, qtdeCidades = lerDistancias(str(saida))
        return distancias, qtdeCidades, pontos

    return _converte
