"""
Converte uma matriz de pontos (R = origem, A-Z = entregas, 0 = vazio)
para o formato de matriz triangular superior de distancias usado
por lerBrasil58.py.

Uso:
    python conversorMatrizParaDistancias.py <entrada.txt> <saida.tsp>

Formato de entrada:
    <linhas> <colunas>
    <matriz com 0 para vazio e letras para pontos>

Exemplo:
    4 5
    0 0 0 0 D
    0 A 0 0 0
    0 0 0 0 C
    R 0 B 0 0
"""

import sys


def lerPontos(arquivo):
	with open(arquivo) as f:
		linhas = [l for l in f.read().splitlines() if l.strip()]

	pontos = {}
	for i, linha in enumerate(linhas[1:]):
		for j, elem in enumerate(linha.split()):
			if elem == "0":
				continue
			if elem in pontos:
				raise ValueError(f"ponto '{elem}' duplicado")
			pontos[elem] = (i, j)

	if "R" not in pontos:
		raise ValueError("ponto de origem 'R' nao encontrado")
	return pontos


def distancia(p1, p2):
	# Distancia de MANHATTAN (|dx| + |dy|): o drone do FLYFOOD so se move na
	# horizontal/vertical da grade ("dronometros"). Tem de ser a MESMA metrica
	# usada pela forca bruta do FLYFOOD, senao os custos/rotas nao batem.
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def gerarMatriz(pontos):
	# R recebe indice 1; demais pontos vem em ordem alfabetica
	ordem = ["R"] + sorted(k for k in pontos if k != "R")
	n = len(ordem)
	return [
		[distancia(pontos[ordem[i]], pontos[ordem[j]]) for j in range(i + 1, n)]
		for i in range(n - 1)
	]


def salvar(arquivo, matriz):
	with open(arquivo, "w") as f:
		for linha in matriz:
			f.write(" ".join(str(d) for d in linha) + "\n")


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Uso: python conversorMatrizParaDistancias.py <entrada.txt> <saida.tsp>")
		sys.exit(1)

	entrada, saida = sys.argv[1], sys.argv[2]
	pontos = lerPontos(entrada)
	matriz = gerarMatriz(pontos)
	salvar(saida, matriz)
	print(f"{len(pontos)} cidades -> {saida}")
