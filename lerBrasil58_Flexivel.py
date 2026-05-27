"""
Versão flexível de lerBrasil58.py que funciona com qualquer número de cidades.
Detecta automaticamente o número de cidades pelo arquivo de entrada.
"""

def ler_arquivo_distancias(caminho_arquivo):
    """
    Lê arquivo de distâncias (UPPER_ROW) e detecta automaticamente 
    o número de cidades pelo número de linhas no arquivo.
    
    Args:
        caminho_arquivo: caminho do arquivo de distâncias
        
    Returns:
        tuple: (distancias_dict, num_cidades)
    """
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas_arquivo = [linha.strip() for linha in f.readlines() if linha.strip()]
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado!")
        return {}, 0
    
    # Detecta número de cidades
    # Para n cidades, matriz triangular superior tem n-1 linhas
    num_linhas = len(linhas_arquivo)
    num_cidades = num_linhas + 1
    
    distancias = {}
    
    # Lê cada linha
    for i in range(1, num_cidades):
        # i começa em 1 (primeira cidade)
        if i - 1 >= len(linhas_arquivo):
            print(f"Erro! Número insuficiente de linhas no arquivo (esperado {num_cidades - 1}, encontrado {num_linhas})")
            return {}, 0
        
        linha = linhas_arquivo[i - 1]
        lista = linha.split()
        
        # Cada linha i deve ter (num_cidades - i) elementos
        elementos_esperados = num_cidades - i
        
        if len(lista) != elementos_esperados:
            print(f"Erro! Linha {i}: esperado {elementos_esperados} elementos, encontrado {len(lista)}")
            print(f"  Conteúdo: {linha}")
            return {}, 0
        
        # Processa cada distância
        for j in range(i + 1, num_cidades + 1):
            if len(lista) > 0:
                peso = int(lista.pop(0))
            else:
                print(f"Erro! Linha {i}: não possui elementos suficientes para coluna {j}")
                return {}, 0
            
            # Grava a aresta em (i, j) e (j, i)
            distancias[(i, j)] = peso
            distancias[(j, i)] = peso
    
    return distancias, num_cidades


def carregar_distancias(nome_arquivo="exemplo_entrada_edges.tsp"):
    """
    Carrega distâncias de um arquivo automaticamente.
    
    Args:
        nome_arquivo: nome do arquivo de distâncias
        
    Returns:
        tuple: (distancias_dict, num_cidades)
    """
    print(f"Carregando distâncias de: {nome_arquivo}")
    distancias, num_cidades = ler_arquivo_distancias(nome_arquivo)
    
    if distancias:
        print(f"✓ Arquivo carregado com sucesso!")
        print(f"  Número de cidades: {num_cidades}")
        return distancias, num_cidades
    else:
        print(f"✗ Erro ao carregar arquivo!")
        return {}, 0


# Carrega automaticamente se foi especificado no início do arquivo
distancias = {}
num_cidades = 0

try:
    distancias, num_cidades = ler_arquivo_distancias("exemplo_entrada_edges.tsp")
except Exception as e:
    print(f"Erro ao carregar arquivo padrão: {e}")
    distancias = {}
    num_cidades = 0


def custoCaminho(permutacao, dicDistancias):
    """
    Calcula o custo total de uma permutação (rota).
    
    Args:
        permutacao: lista com a ordem das cidades [1, 3, 2, 4, ...]
        dicDistancias: dicionário de distâncias {(i,j): distância}
        
    Returns:
        int: custo total da rota
    """
    if not permutacao:
        return 0
    
    soma = 0
    for i in range(len(permutacao) - 1):
        a = permutacao[i]
        b = permutacao[i + 1]
        if (a, b) in dicDistancias:
            soma += dicDistancias[(a, b)]
        else:
            print(f"Erro! ({a},{b}) não existe no dicionário!")
            exit()
    
    # Volta à cidade inicial
    soma += dicDistancias[(permutacao[-1], permutacao[0])]
    return soma


def inicializaPopulacao(tamanho, qtdeCidades):
    """
    Cria população inicial com indivíduos aleatórios.
    
    Args:
        tamanho: número de indivíduos na população
        qtdeCidades: número de cidades (permutação será 1 a qtdeCidades)
        
    Returns:
        list: lista de listas com permutações aleatórias
    """
    import random
    lista = []
    for i in range(tamanho):
        individuo = list(range(1, qtdeCidades + 1))
        random.shuffle(individuo)
        lista.append(individuo)
    return lista


def calculaAptidao(populacao, dicDistancias):
    """
    Calcula o fitness (aptidão) de todos os indivíduos da população.
    
    Args:
        populacao: lista de permutações (indivíduos)
        dicDistancias: dicionário de distâncias
        
    Returns:
        list: lista com o custo (fitness) de cada indivíduo
    """
    aptidoes = []
    for individuo in populacao:
        custo = custoCaminho(individuo, dicDistancias)
        aptidoes.append(custo)
    return aptidoes


# Informações sobre o arquivo
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Leitor de Distâncias - Versão Flexível")
    print("="*60)
    
    print(f"\nArquivo carregado: exemplo_entrada_edges.tsp")
    print(f"Número de cidades: {num_cidades}")
    print(f"Número de distâncias: {len(distancias) // 2}")  # divide por 2 pois armazena (i,j) e (j,i)
    
    if distancias and num_cidades > 0:
        # Mostra algumas distâncias
        print("\nExemplo de distâncias:")
        for i in range(1, min(4, num_cidades)):
            for j in range(i+1, min(4, num_cidades+1)):
                if (i, j) in distancias:
                    print(f"  d({i},{j}) = {distancias[(i,j)]}")
