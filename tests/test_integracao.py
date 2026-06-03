"""Testes de integracao (ponta a ponta) do Algoritmo Genetico.

Dois cenarios, conforme as metas do projeto:
  1. Resolver a instancia BRASIL58 e chegar perto do otimo conhecido.
  2. Resolver uma GRADE do FLYFOOD (texto -> conversor -> GA) e comparar
     com a FORCA BRUTA (otimo exato), exatamente o "A.G. versus FORCA
     BRUTA" do quadro.

Os testes usam poucas geracoes (para serem rapidos) e 'verbose=False'
(para nao poluir a saida). Cada teste emite apenas um resumo via log.
"""

import logging
import random

import algoritmoGeneticoBrasil58 as ag

log = logging.getLogger(__name__)

OTIMO_BRASIL58 = 25395


def test_resolve_brazil58_chega_perto_do_otimo():
    """O GA deve produzir uma rota valida e bem melhor que o acaso."""
    random.seed(123)  # resultado reproduzivel

    rota, custo = ag.algoritmoGenetico(numGeracoes=800, verbose=False)

    # 1) a rota e valida: passa pelas 58 cidades exatamente uma vez
    assert sorted(rota) == list(range(1, 59)), "rota deve ser permutacao de 1..58"

    gap = (custo - OTIMO_BRASIL58) / OTIMO_BRASIL58 * 100
    log.info("Brasil58 (800 ger): custo=%d | otimo=%d | gap=%.1f%%",
             custo, OTIMO_BRASIL58, gap)

    # 2) otimizou de fato (rotas aleatorias custam dezenas de milhares a mais)
    assert custo < 40000
    # 3) chegou perto do otimo conhecido
    assert gap < 10, f"gap {gap:.1f}% acima do esperado"


def test_resolve_grade_convertida_bate_forca_bruta(converte_grade, forca_bruta):
    """Pipeline completo: grade de texto -> conversor -> GA == forca bruta."""
    grade = (
        "4 5\n"
        "0 0 0 0 D\n"
        "0 A 0 0 0\n"
        "0 0 0 0 C\n"
        "R 0 B 0 0\n"
    )

    distancias, qtdeCidades, pontos = converte_grade(grade)
    otimo = forca_bruta(qtdeCidades, distancias)

    random.seed(0)
    rota, custo = ag.algoritmoGenetico(
        distancias, qtdeCidades,
        numGeracoes=300, tamanhoPopulacao=30, numFilhos=15, verbose=False,
    )

    assert sorted(rota) == list(range(1, qtdeCidades + 1)), "rota deve ser valida"
    log.info("Grade %d pontos %s: GA=%d | forca bruta=%d",
             qtdeCidades, sorted(pontos), custo, otimo)

    # problema pequeno: o GA tem de encontrar o OTIMO exato
    assert custo == otimo, "GA deveria achar o otimo em instancia pequena"


def test_resolve_segunda_grade_bate_forca_bruta(converte_grade, forca_bruta):
    """Uma grade diferente, com 6 pontos, para reforcar o teste anterior."""
    grade = (
        "4 4\n"
        "R 0 0 A\n"
        "0 B 0 0\n"
        "0 0 C D\n"
        "E 0 0 0\n"
    )

    distancias, qtdeCidades, pontos = converte_grade(grade, nome="grade6")
    otimo = forca_bruta(qtdeCidades, distancias)

    random.seed(7)
    rota, custo = ag.algoritmoGenetico(
        distancias, qtdeCidades,
        numGeracoes=400, tamanhoPopulacao=40, numFilhos=20, verbose=False,
    )

    assert sorted(rota) == list(range(1, qtdeCidades + 1))
    log.info("Grade %d pontos %s: GA=%d | forca bruta=%d",
             qtdeCidades, sorted(pontos), custo, otimo)
    assert custo == otimo
