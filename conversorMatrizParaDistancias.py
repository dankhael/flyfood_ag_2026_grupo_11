"""
Conversor de Matriz de Pontos para Matriz Triangular Superior de Distâncias

Formato de entrada esperado (entrada.txt):
    <linhas> <colunas>
    <matriz com '0' para vazio e letras para pontos>
    
    Exemplo:
    4 5
    0 0 0 0 D
    0 A 0 0 0
    0 0 0 0 C
    R 0 B 0 0
    
    Onde:
    - R = origem e retorno do drone (obrigatório)
    - A, B, C, D... = pontos de entrega
    - 0 = posição vazia

Saída: Arquivo .txt com matriz triangular superior de distâncias (UPPER_ROW)
"""

import sys
import math
from pathlib import Path


def ler_matriz_pontos(caminho_arquivo):
    """
    Lê o arquivo no formato especificado e extrai as coordenadas dos pontos.
    
    Retorna:
        dict: mapa de {letra: (linha, coluna)}
        int: número total de pontos
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.read().strip().split('\n')
        
        # Primeira linha: dimensões
        dimensoes = linhas[0].split()
        num_linhas = int(dimensoes[0])
        num_colunas = int(dimensoes[1])
        
        pontos = {}
        
        # Processa a matriz
        for i in range(1, num_linhas + 1):
            elementos = linhas[i].split()
            
            if len(elementos) != num_colunas:
                print(f"Erro na linha {i}: esperado {num_colunas} colunas, encontrado {len(elementos)}")
                return None, 0
            
            for j, elemento in enumerate(elementos):
                if elemento != '0':
                    if elemento in pontos:
                        print(f"Erro: ponto '{elemento}' duplicado em ({i-1}, {j})")
                        return None, 0
                    pontos[elemento] = (i - 1, j)  # i-1 pois a matriz começa na linha 1
        
        # Valida se existe o ponto de origem 'R'
        if 'R' not in pontos:
            print("Erro: ponto de origem 'R' não encontrado na matriz!")
            return None, 0
        
        return pontos, len(pontos)
    
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado!")
        return None, 0
    except ValueError as e:
        print(f"Erro ao processar arquivo: {e}")
        return None, 0


def calcular_distancia_euclidiana(p1, p2):
    """
    Calcula a distância euclidiana entre dois pontos.
    
    Args:
        p1, p2: tuplas (linha, coluna)
    
    Retorna:
        float: distância entre os pontos
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def gerar_matriz_distancias(pontos):
    """
    Gera a matriz triangular superior de distâncias.
    
    Args:
        pontos: dict de {letra: (linha, coluna)}
    
    Retorna:
        dict: matriz de distâncias {(i, j): distância}
        list: lista ordenada de letras das cidades
    """
    # Ordena os pontos: R primeiro (índice 1), depois os demais em ordem alfabética
    cidades_ordenadas = ['R'] + sorted([k for k in pontos.keys() if k != 'R'])
    
    # Cria mapa de índices
    indice_cidade = {cidade: idx + 1 for idx, cidade in enumerate(cidades_ordenadas)}
    
    # Calcula distâncias
    distancias = {}
    num_cidades = len(cidades_ordenadas)
    
    for i in range(num_cidades):
        for j in range(i + 1, num_cidades):
            cidade_i = cidades_ordenadas[i]
            cidade_j = cidades_ordenadas[j]
            
            dist = calcular_distancia_euclidiana(pontos[cidade_i], pontos[cidade_j])
            dist_int = int(round(dist))  # Arredonda para inteiro
            
            idx_i = indice_cidade[cidade_i]
            idx_j = indice_cidade[cidade_j]
            
            distancias[(idx_i, idx_j)] = dist_int
            distancias[(idx_j, idx_i)] = dist_int
    
    return distancias, cidades_ordenadas, indice_cidade


def salvar_matriz_tsp(caminho_saida, distancias, num_cidades, nome_problema="ConvertedProblem"):
    """
    Salva a matriz de distâncias no formato TSP (UPPER_ROW).
    
    Args:
        caminho_saida: caminho do arquivo de saída
        distancias: dict com as distâncias
        num_cidades: número de cidades
        nome_problema: nome do problema TSP
    """
    try:
        with open(caminho_saida, 'w') as f:
            # Cabeçalho TSP
            f.write(f"NAME: {nome_problema}\n")
            f.write("TYPE: TSP\n")
            f.write(f"DIMENSION: {num_cidades}\n")
            f.write("EDGE_WEIGHT_TYPE: EXPLICIT\n")
            f.write("EDGE_WEIGHT_FORMAT: UPPER_ROW\n")
            f.write("EDGE_WEIGHT_SECTION\n")
            
            # Matriz triangular superior
            for i in range(1, num_cidades):
                linha_distancias = []
                for j in range(i + 1, num_cidades + 1):
                    if (i, j) in distancias:
                        linha_distancias.append(str(distancias[(i, j)]))
                    else:
                        print(f"Aviso: distância entre {i} e {j} não encontrada!")
                        linha_distancias.append("0")
                
                f.write(" ".join(linha_distancias) + "\n")
        
        print(f"✓ Arquivo TSP salvo com sucesso em: {caminho_saida}")
        return True
    
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False


def salvar_matriz_edges(caminho_saida, distancias, num_cidades):
    """
    Salva apenas a matriz triangular superior (formato simplificado).
    
    Args:
        caminho_saida: caminho do arquivo de saída
        distancias: dict com as distâncias
        num_cidades: número de cidades
    """
    try:
        with open(caminho_saida, 'w') as f:
            for i in range(1, num_cidades):
                linha_distancias = []
                for j in range(i + 1, num_cidades + 1):
                    if (i, j) in distancias:
                        linha_distancias.append(str(distancias[(i, j)]))
                    else:
                        linha_distancias.append("0")
                
                f.write(" ".join(linha_distancias) + "\n")
        
        print(f"✓ Arquivo EDGES salvo com sucesso em: {caminho_saida}")
        return True
    
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False


def converter_arquivo(arquivo_entrada, arquivo_saida_tsp=None, arquivo_saida_edges=None):
    """
    Função principal que orquestra todo o processo de conversão.
    
    Args:
        arquivo_entrada: caminho do arquivo de entrada
        arquivo_saida_tsp: caminho opcional para arquivo TSP completo
        arquivo_saida_edges: caminho opcional para arquivo EDGES
    """
    print("=" * 60)
    print("Conversor de Matriz de Pontos para Distâncias TSP")
    print("=" * 60)
    
    # Lê a matriz de pontos
    print(f"\n1. Lendo arquivo: {arquivo_entrada}")
    pontos, num_pontos = ler_matriz_pontos(arquivo_entrada)
    
    if pontos is None:
        return False
    
    print(f"   ✓ {num_pontos} pontos encontrados")
    for letra, coord in sorted(pontos.items()):
        print(f"      {letra}: linha {coord[0]}, coluna {coord[1]}")
    
    # Calcula distâncias
    print("\n2. Calculando matriz de distâncias...")
    distancias, cidades, indice = gerar_matriz_distancias(pontos)
    print(f"   ✓ Matriz calculada com sucesso")
    print(f"   Cidades ordenadas: {', '.join(cidades)}")
    
    # Define nomes de arquivo padrão se não fornecidos
    if arquivo_saida_tsp is None:
        base_saida = Path(arquivo_entrada).stem
        arquivo_saida_tsp = f"{base_saida}_distancias.tsp"
    
    if arquivo_saida_edges is None:
        base_saida = Path(arquivo_entrada).stem
        arquivo_saida_edges = f"{base_saida}_edges.tsp"
    
    # Salva arquivos de saída
    print(f"\n3. Salvando arquivos de saída...")
    
    nome_problema = Path(arquivo_entrada).stem.replace('_', ' ').title()
    
    sucesso_tsp = salvar_matriz_tsp(
        arquivo_saida_tsp,
        distancias,
        num_pontos,
        nome_problema
    )
    
    sucesso_edges = salvar_matriz_edges(
        arquivo_saida_edges,
        distancias,
        num_pontos
    )
    
    print("\n" + "=" * 60)
    print("Conversão concluída com sucesso!")
    print("=" * 60)
    
    return sucesso_tsp and sucesso_edges


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python conversorMatrizParaDistancias.py <arquivo_entrada> [arquivo_saida_tsp] [arquivo_saida_edges]")
        print("\nExemplo:")
        print("  python conversorMatrizParaDistancias.py entrada.txt")
        print("  python conversorMatrizParaDistancias.py entrada.txt saida.tsp saida_edges.tsp")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida_tsp = sys.argv[2] if len(sys.argv) > 2 else None
    arquivo_saida_edges = sys.argv[3] if len(sys.argv) > 3 else None
    
    converter_arquivo(arquivo_entrada, arquivo_saida_tsp, arquivo_saida_edges)
