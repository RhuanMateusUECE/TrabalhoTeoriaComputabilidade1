# tests.py
"""
Módulo para testes das implementações.
Este arquivo contém funções para testar cada etapa da implementação separadamente.
"""

import os
from automato import AutomatoFinitoDeterministico, AutomatoFinitoNaoDeterministico
from glud_to_afn import converter_glud_para_afn
from afn_to_afd import converter_afn_para_afd
from operations import aplicar_reverso, aplicar_complemento
from simulation import simular_cadeia_detalhada

def criar_arquivo_gramatica_exemplo():
    """
    Cria um arquivo de exemplo com uma gramática GLUD para testes.
    
    Returns:
        str: Nome do arquivo criado.
    """
    nome_arquivo = "gramatica_exemplo.txt"
    
    conteudo = """# Gramática: G = ({S, A}, {a, b}, P, S)

S -> aA
A -> bS
S -> ε
"""
    
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)
    
    print(f"Arquivo de exemplo '{nome_arquivo}' criado com sucesso.")
    return nome_arquivo

def testar_glud_para_afn(arquivo_gramatica):
    """
    Testa a conversão de GLUD para AFN.
    
    Args:
        arquivo_gramatica (str): Caminho do arquivo contendo a gramática.
        
    Returns:
        AutomatoFinitoNaoDeterministico: AFN gerado.
    """
    print("\n===== Teste de Conversão GLUD -> AFN =====")
    afn = converter_glud_para_afn(arquivo_gramatica)
    
    print("AFN gerado:")
    print(afn)
    
    # Salvar a representação do AFN em um arquivo
    with open("AFN.txt", 'w', encoding='utf-8') as arquivo:
        arquivo.write(afn.obter_representacao_texto())
    
    print("Arquivo 'AFN.txt' gerado com sucesso.")
    
    return afn

def testar_afn_para_afd(afn):
    """
    Testa a conversão de AFN para AFD.
    
    Args:
        afn: AutomatoFinitoNaoDeterministico a ser convertido.
        
    Returns:
        AutomatoFinitoDeterministico: AFD gerado.
    """
    print("\n===== Teste de Conversão AFN -> AFD =====")
    afd = converter_afn_para_afd(afn)
    
    print("AFD gerado:")
    print(afd)
    
    # Salvar a representação do AFD em um arquivo
    with open("AFD.txt", 'w', encoding='utf-8') as arquivo:
        arquivo.write(afd.obter_representacao_texto())
    
    print("Arquivo 'AFD.txt' gerado com sucesso.")
    
    return afd

def testar_operacoes_fecho(afd):
    """
    Testa as operações de fecho (reverso e complemento).
    
    Args:
        afd: AutomatoFinitoDeterministico a ser usado nas operações.
        
    Returns:
        tuple: (afd_reverso, afd_complemento)
    """
    print("\n===== Teste de Operações de Fecho =====")
    
    # Testar operação de reverso
    print("\n--- Operação de Reverso ---")
    afd_reverso = aplicar_reverso(afd)
    
    print("AFD Reverso:")
    print(afd_reverso)
    
    # Salvar a representação do AFD Reverso em um arquivo
    with open("REV.txt", 'w', encoding='utf-8') as arquivo:
        arquivo.write(afd_reverso.obter_representacao_texto())
    
    print("Arquivo 'REV.txt' gerado com sucesso.")
    
    # Testar operação de complemento
    print("\n--- Operação de Complemento ---")
    afd_complemento = aplicar_complemento(afd)
    
    print("AFD Complemento:")
    print(afd_complemento)
    
    # Salvar a representação do AFD Complemento em um arquivo
    with open("COMP.txt", 'w', encoding='utf-8') as arquivo:
        arquivo.write(afd_complemento.obter_representacao_texto())
    
    print("Arquivo 'COMP.txt' gerado com sucesso.")
    
    return afd_reverso, afd_complemento

def testar_simulacao(afd, cadeia):
    """
    Testa a simulação de uma cadeia em um AFD.
    
    Args:
        afd: AutomatoFinitoDeterministico a ser usado na simulação.
        cadeia (str): Cadeia a ser simulada.
        
    Returns:
        bool: True se a cadeia foi aceita, False caso contrário.
    """
    print(f"\n===== Teste de Simulação (Cadeia: '{cadeia}') =====")
    
    return simular_cadeia_detalhada(afd, cadeia)

def executar_testes():
    """
    Executa todos os testes em sequência.
    """
    # Criar arquivo de gramática de exemplo
    arquivo_gramatica = criar_arquivo_gramatica_exemplo()
    
    # Testar conversão de GLUD para AFN
    afn = testar_glud_para_afn(arquivo_gramatica)
    
    # Testar conversão de AFN para AFD
    afd = testar_afn_para_afd(afn)
    
    # Testar operações de fecho
    afd_reverso, afd_complemento = testar_operacoes_fecho(afd)
    
    # Testar simulação de cadeias
    cadeias_teste = ["", "a", "ab", "aba", "abab", "ababab"]
    
    print("\n===== Testes de Simulação =====")
    
    print("\n--- AFD Original ---")
    for cadeia in cadeias_teste:
        aceita = testar_simulacao(afd, cadeia)
        print(f"Cadeia '{cadeia}': {'Aceita' if aceita else 'Rejeitada'}")
    
    print("\n--- AFD Reverso ---")
    for cadeia in cadeias_teste:
        aceita = testar_simulacao(afd_reverso, cadeia)
        print(f"Cadeia '{cadeia}': {'Aceita' if aceita else 'Rejeitada'}")
    
    print("\n--- AFD Complemento ---")
    for cadeia in cadeias_teste:
        aceita = testar_simulacao(afd_complemento, cadeia)
        print(f"Cadeia '{cadeia}': {'Aceita' if aceita else 'Rejeitada'}")
    
    print("\nTodos os testes foram concluídos com sucesso.")

if __name__ == "__main__":
    executar_testes()