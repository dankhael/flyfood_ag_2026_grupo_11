"""Testes do conversor de grade (FLYFOOD) -> matriz de distancias.

Cobrem a leitura dos pontos da grade, as validacoes de entrada, o calculo
de distancia euclidiana e o formato da matriz triangular superior gerada.
"""

import logging

import pytest

import conversorMatrizParaDistancias as conv

log = logging.getLogger(__name__)


def test_ler_pontos_detecta_coordenadas(tmp_path):
    arquivo = tmp_path / "grade.txt"
    # 1a linha = dimensoes (ignorada na leitura dos pontos)
    arquivo.write_text("2 3\nR 0 A\n0 B 0\n")

    pontos = conv.lerPontos(str(arquivo))

    assert pontos["R"] == (0, 0)
    assert pontos["A"] == (0, 2)
    assert pontos["B"] == (1, 1)
    log.info("Conversor: pontos lidos = %s", pontos)


def test_ler_pontos_exige_origem_R(tmp_path):
    arquivo = tmp_path / "grade.txt"
    arquivo.write_text("1 2\nA B\n")
    with pytest.raises(ValueError):
        conv.lerPontos(str(arquivo))


def test_ler_pontos_rejeita_ponto_duplicado(tmp_path):
    arquivo = tmp_path / "grade.txt"
    arquivo.write_text("1 3\nR A A\n")
    with pytest.raises(ValueError):
        conv.lerPontos(str(arquivo))


def test_distancia_euclidiana_arredondada():
    assert conv.distancia((0, 0), (3, 4)) == 5      # 3-4-5
    assert conv.distancia((0, 0), (1, 1)) == 1      # round(1.414) = 1


def test_matriz_tem_formato_triangular_superior():
    pontos = {"R": (0, 0), "A": (0, 3), "B": (4, 0)}
    matriz = conv.gerarMatriz(pontos)
    # com n=3 pontos, as linhas devem ter 2 e 1 entradas (n-1, n-2, ...)
    assert [len(linha) for linha in matriz] == [2, 1]
    log.info("Conversor: matriz triangular = %s", matriz)


def test_exemplo_entrada_do_repo_converte(tmp_path):
    # garante que o arquivo de exemplo versionado continua valido
    pontos = conv.lerPontos("exemplo_entrada.txt")
    assert "R" in pontos and len(pontos) == 5
    matriz = conv.gerarMatriz(pontos)
    assert len(matriz) == len(pontos) - 1
