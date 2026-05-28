import os
import random

# Permite escolher outro arquivo via variavel de ambiente sem editar codigo:
#   PowerShell : $env:ARQUIVO_TSP = "meu_problema.tsp"
#   bash       : ARQUIVO_TSP=meu_problema.tsp python algoritmoGeneticoBrasil58.py
NOME_ARQUIVO = os.environ.get("ARQUIVO_TSP", "edgesbrasil58.tsp")


def lerDistancias(arquivo):
	"""Le matriz triangular superior de distancias.

	Detecta o numero de cidades pela quantidade de linhas do arquivo
	(uma matriz triangular superior de n cidades tem n-1 linhas).
	"""
	with open(arquivo) as f:
		linhas = [l.split() for l in f if l.strip()]

	qtdeCidades = len(linhas) + 1
	distancias = {}
	for i, lista in enumerate(linhas, start=1):
		for j in range(i + 1, qtdeCidades + 1):
			peso = int(lista.pop(0))
			distancias[(i, j)] = peso
			distancias[(j, i)] = peso
	return distancias, qtdeCidades


distancias, qtdeCidades = lerDistancias(NOME_ARQUIVO)


def custoCaminho(permutacao, dicDistancias):
	soma = 0
	for i in range(len(permutacao) - 1):
		soma += dicDistancias[(permutacao[i], permutacao[i + 1])]
	soma += dicDistancias[(permutacao[-1], permutacao[0])]
	return soma


def inicializaPopulacao(tamanho, qtdeCidades):
	lista = []
	for _ in range(tamanho):
		individuo = list(range(1, qtdeCidades + 1))
		random.shuffle(individuo)
		lista.append(individuo)
	return lista


def calculaAptidao(populacao, dicDistancias):
	return [custoCaminho(ind, dicDistancias) for ind in populacao]
