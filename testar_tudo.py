#!/usr/bin/env python3
"""
Script de teste: verifica se o conversor e algoritmo funcionam corretamente
"""

import sys
import os

print("\n" + "="*70)
print("TESTE COMPLETO: CONVERSOR + ALGORITMO GENÉTICO")
print("="*70)

# Teste 1: Verificar arquivo convertido
print("\n1. Verificando arquivo convertido...")
if os.path.exists("exemplo_entrada_edges.tsp"):
    with open("exemplo_entrada_edges.tsp", 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
    print(f"   ✓ Arquivo encontrado com {len(linhas)} linhas")
    for i, linha in enumerate(linhas, 1):
        elementos = len(linha.split())
        print(f"     Linha {i}: {elementos} elementos")
else:
    print("   ✗ Arquivo não encontrado!")
    sys.exit(1)

# Teste 2: Carregar distâncias
print("\n2. Carregando distâncias com lerBrasil58_Flexivel...")
try:
    from lerBrasil58_Flexivel import ler_arquivo_distancias
    distancias, num_cidades = ler_arquivo_distancias("exemplo_entrada_edges.tsp")
    
    if distancias and num_cidades > 0:
        print(f"   ✓ Carregado com sucesso!")
        print(f"     Número de cidades: {num_cidades}")
        print(f"     Número de distâncias: {len(distancias) // 2}")
        
        # Mostra algumas distâncias
        print(f"     Exemplos:")
        for i in range(1, min(3, num_cidades)):
            for j in range(i+1, min(i+2, num_cidades+1)):
                if (i, j) in distancias:
                    print(f"       d({i},{j}) = {distancias[(i,j)]}")
    else:
        print("   ✗ Erro ao carregar distâncias!")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

# Teste 3: Executar algoritmo genético
print("\n3. Executando algoritmo genético...")
try:
    from algoritmoGeneticoFlexivel import algoritmoGeneticoFlexivel
    
    melhorRota, melhorCusto, num_cidades_ag = algoritmoGeneticoFlexivel(
        arquivo_distancias="exemplo_entrada_edges.tsp",
        tamanho_populacao=30,
        num_geracoes=100
    )
    
    if melhorRota is not None:
        print(f"\n   ✓ Algoritmo executado com sucesso!")
        print(f"     Melhor custo encontrado: {melhorCusto}")
        print(f"     Rota: {melhorRota}")
    else:
        print("   ✗ Erro na execução do algoritmo!")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70)
print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("="*70)
print("\nPróximos passos:")
print("1. Modifique o arquivo de entrada conforme necessário")
print("2. Execute: python algoritmoGeneticoFlexivel.py")
print("3. Ou use ARQUIVO_DISTANCIAS no código para alterar o arquivo")
print()
