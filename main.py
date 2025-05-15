# main.py
"""
Simulador de Autômato Finito com Operações e Gramática Linear à Direita
Disciplina: Teoria da Computação

Este é o módulo principal que coordena as operações do simulador.
"""
import os
import sys
from glud_to_afn import converter_glud_para_afn
from afn_to_afd import converter_afn_para_afd
from operations import aplicar_reverso, aplicar_complemento
from simulation import simular_cadeia_detalhada, visualizar_tabela_transicoes

def main():
    """Função principal que coordena o fluxo do programa."""
    print("\n====================================================================")
    print("  SIMULADOR DE AUTÔMATO FINITO COM OPERAÇÕES E GRAMÁTICA LINEAR")
    print("====================================================================\n")
    
    # Verificar se o caminho do arquivo foi fornecido
    if len(sys.argv) != 3:
        print("Uso: python main.py arquivo_gramatica.txt cadeia_entrada")
        return
    
    arquivo_gramatica = sys.argv[1]
    cadeia_entrada = sys.argv[2]
    
    # Verificar se o arquivo de gramática existe
    if not os.path.exists(arquivo_gramatica):
        print(f"Erro: O arquivo {arquivo_gramatica} não existe.")
        return
    
    try:
        # Etapa 1: Converter GLUD para AFN
        print("\n[ETAPA 1] CONVERTENDO GLUD PARA AFN")
        print("-" * 70)
        print(f"Arquivo de entrada: {arquivo_gramatica}")
        afn = converter_glud_para_afn(arquivo_gramatica)
        print(f"AFN gerado com sucesso!")
        print(f"  - Estados: {len(afn.estados)}")
        print(f"  - Símbolos do alfabeto: {len(afn.alfabeto)}")
        print(f"  - Transições: {len(afn.transicoes)}")
        
        # Exibir a tabela de transições do AFN
        visualizar_tabela_transicoes(afn)
        
        # Salvar a representação do AFN
        nome_arquivo_afn = "AFN.txt"
        salvar_automato(afn, nome_arquivo_afn)
        print(f"Arquivo '{nome_arquivo_afn}' gerado com sucesso.")
        
        # Etapa 2: Converter AFN para AFD
        print("\n[ETAPA 2] CONVERTENDO AFN PARA AFD")
        print("-" * 70)
        afd = converter_afn_para_afd(afn)
        print(f"AFD gerado com sucesso!")
        print(f"  - Estados: {len(afd.estados)}")
        print(f"  - Símbolos do alfabeto: {len(afd.alfabeto)}")
        print(f"  - Transições: {len(afd.transicoes)}")
        
        # Exibir a tabela de transições do AFD
        visualizar_tabela_transicoes(afd)
        
        # Salvar a representação do AFD
        nome_arquivo_afd = "AFD.txt"
        salvar_automato(afd, nome_arquivo_afd)
        print(f"Arquivo '{nome_arquivo_afd}' gerado com sucesso.")
        
        # Etapa 3: Aplicar operações de fecho
        print("\n[ETAPA 3] APLICANDO OPERAÇÕES DE FECHO")
        print("-" * 70)
        
        # Operação de Reverso
        print("\n[3.1] Operação de Reverso")
        afd_reverso = aplicar_reverso(afd)
        print(f"AFD Reverso gerado com sucesso!")
        print(f"  - Estados: {len(afd_reverso.estados)}")
        print(f"  - Símbolos do alfabeto: {len(afd_reverso.alfabeto)}")
        print(f"  - Transições: {len(afd_reverso.transicoes)}")
        
        # Exibir a tabela de transições do AFD Reverso
        visualizar_tabela_transicoes(afd_reverso)
        
        # Salvar a representação do AFD Reverso
        nome_arquivo_reverso = "REV.txt"
        salvar_automato(afd_reverso, nome_arquivo_reverso)
        print(f"Arquivo '{nome_arquivo_reverso}' gerado com sucesso.")
        
        # Operação de Complemento
        print("\n[3.2] Operação de Complemento")
        afd_complemento = aplicar_complemento(afd)
        print(f"AFD Complemento gerado com sucesso!")
        print(f"  - Estados: {len(afd_complemento.estados)}")
        print(f"  - Símbolos do alfabeto: {len(afd_complemento.alfabeto)}")
        print(f"  - Transições: {len(afd_complemento.transicoes)}")
        
        # Exibir a tabela de transições do AFD Complemento
        visualizar_tabela_transicoes(afd_complemento)
        
        # Salvar a representação do AFD Complemento
        nome_arquivo_complemento = "COMP.txt"
        salvar_automato(afd_complemento, nome_arquivo_complemento)
        print(f"Arquivo '{nome_arquivo_complemento}' gerado com sucesso.")
        
        # Etapa 4: Simular cadeia
        print("\n[ETAPA 4] SIMULANDO CADEIA DE ENTRADA")
        print("-" * 70)
        print(f"Cadeia de entrada: '{cadeia_entrada}'")
        
        # Simular a cadeia no AFD
        aceita = simular_cadeia_detalhada(afd, cadeia_entrada)
        
        # Resultado final
        print("\n====================================================================")
        print("  RESULTADO FINAL")
        print("====================================================================")
        print(f"Cadeia de entrada: '{cadeia_entrada}'")
        if aceita:
            print("✅ ACEITA pelo AFD original")
        else:
            print("❌ REJEITADA pelo AFD original")
        
        print(f"\nArquivos gerados:")
        print(f"  - {nome_arquivo_afn} (AFN gerado a partir da gramática)")
        print(f"  - {nome_arquivo_afd} (AFD determinizado)")
        print(f"  - {nome_arquivo_reverso} (AFD após operação de reverso)")
        print(f"  - {nome_arquivo_complemento} (AFD após operação de complemento)")
        
        # Oferecer simulação nos outros autômatos
        print("\nDeseja simular a cadeia nos outros autômatos? (s/n): ", end="")
        resposta = input().strip().lower()
        
        if resposta == 's':
            # Simular a cadeia no AFD Reverso
            print("\nSimulação no AFD Reverso:")
            aceita_reverso = simular_cadeia_detalhada(afd_reverso, cadeia_entrada)
            
            # Simular a cadeia no AFD Complemento
            print("\nSimulação no AFD Complemento:")
            aceita_complemento = simular_cadeia_detalhada(afd_complemento, cadeia_entrada)
            
            # Resumo das simulações
            print("\n====================================================================")
            print("  RESUMO DAS SIMULAÇÕES")
            print("====================================================================")
            print(f"Cadeia: '{cadeia_entrada}'")
            print(f"  - AFD Original: {'ACEITA' if aceita else 'REJEITADA'}")
            print(f"  - AFD Reverso: {'ACEITA' if aceita_reverso else 'REJEITADA'}")
            print(f"  - AFD Complemento: {'ACEITA' if aceita_complemento else 'REJEITADA'}")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

def salvar_automato(automato, nome_arquivo):
    """Salva a representação do autômato em um arquivo de texto."""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(automato.obter_representacao_texto())

if __name__ == "__main__":
    main()