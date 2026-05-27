import random
from algoritmoGeneticoBrasil58 import algoritmoGenetico

VALOR_DESEJADO = 25395
DESVIO_PERMITIDO = 1
NUM_TESTES = 10

if __name__ == "__main__":
    random.seed()
    media = []
    sucesso = []
    for i in range(NUM_TESTES):
        melhorRota, melhorCusto = algoritmoGenetico()
        media.append(melhorCusto)
    for i in media:
        if int(i) < VALOR_DESEJADO + (VALOR_DESEJADO * (DESVIO_PERMITIDO/100)):
            sucesso.append(i)
    porcentagemsucesso = (len(sucesso)/NUM_TESTES) * 100
    print(f"Dentre {NUM_TESTES} testes, {porcentagemsucesso}% dos algoritimos estavam em {DESVIO_PERMITIDO}% de {VALOR_DESEJADO}")