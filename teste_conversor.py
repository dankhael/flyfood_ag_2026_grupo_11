#!/usr/bin/env python3
"""
Script de teste para o conversor de matriz para distâncias.
Executa o conversor em múltiplos arquivos de exemplo e valida os resultados.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from conversorMatrizParaDistancias import converter_arquivo


def testar_conversor():
    """Executa testes do conversor com múltiplos exemplos."""
    
    print("\n" + "=" * 70)
    print("TESTES DO CONVERSOR DE MATRIZ PARA DISTÂNCIAS")
    print("=" * 70)
    
    # Lista de arquivos para testar
    arquivos_teste = [
        "exemplo_entrada.txt",
        "exemplo_grande.txt"
    ]
    
    for arquivo in arquivos_teste:
        caminho_arquivo = Path(arquivo)
        
        if not caminho_arquivo.exists():
            print(f"\n⚠ Arquivo não encontrado: {arquivo}")
            continue
        
        print(f"\n\n{'─' * 70}")
        print(f"TESTE: {arquivo}")
        print('─' * 70)
        
        # Executa a conversão
        resultado = converter_arquivo(arquivo)
        
        if resultado:
            # Verifica os arquivos gerados
            base_nome = caminho_arquivo.stem
            arquivo_tsp = f"{base_nome}_distancias.tsp"
            arquivo_edges = f"{base_nome}_edges.tsp"
            
            print("\n✓ Validando arquivos gerados...")
            
            if Path(arquivo_tsp).exists():
                tamanho_tsp = Path(arquivo_tsp).stat().st_size
                print(f"   {arquivo_tsp}: {tamanho_tsp} bytes")
            
            if Path(arquivo_edges).exists():
                tamanho_edges = Path(arquivo_edges).stat().st_size
                print(f"   {arquivo_edges}: {tamanho_edges} bytes")
        else:
            print("\n✗ Falha na conversão!")
    
    print("\n" + "=" * 70)
    print("TESTES CONCLUÍDOS")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    testar_conversor()
