# simulation.py
"""
Módulo para simulação da execução de cadeias em Autômatos Finitos.
Fornece funções para simular e visualizar o processamento de cadeias.
"""

def simular_cadeia(automato, cadeia):
    """
    Simula a execução de uma cadeia em um autômato finito.
    
    Args:
        automato: AutomatoFinito a ser utilizado na simulação.
        cadeia (str): Cadeia de entrada a ser processada.
        
    Returns:
        bool: True se a cadeia for aceita, False caso contrário.
    """
    # Verificar se o autômato é determinístico
    if not automato.deterministic:
        raise ValueError("A simulação direta só é possível em autômatos determinísticos. " +
                         "Converta o autômato para AFD antes de simular.")
    
    # Inicializar o estado atual como o estado inicial do autômato
    estado_atual = automato.estado_inicial
    
    # Percorrer cada símbolo da cadeia
    print("\n==========================================")
    print("       SIMULAÇÃO PASSO A PASSO")
    print("==========================================")
    
    # Verificar caso especial de cadeia vazia
    if not cadeia:
        print(f"Cadeia de entrada: '' (cadeia vazia)")
    else:
        print(f"Cadeia de entrada: '{cadeia}'")
    
    print("\n> Estado inicial: {0}".format(estado_atual))
    
    for i, simbolo in enumerate(cadeia):
        # Verificar se o símbolo pertence ao alfabeto
        if simbolo not in automato.alfabeto:
            print(f"\n❌ ERRO: O símbolo '{simbolo}' não pertence ao alfabeto do autômato.")
            print("   Alfabeto permitido: {" + ", ".join(sorted(automato.alfabeto)) + "}")
            return False
        
        # Obter o próximo estado
        proximo_estado = automato.obter_transicao_afd(estado_atual, simbolo)
        
        # Verificar se existe uma transição definida
        if proximo_estado is None:
            print(f"\n❌ ERRO: Não há transição definida para o par ({estado_atual}, {simbolo}).")
            return False
        
        print(f"> Passo {i+1}: Lendo '{simbolo}' - δ({estado_atual}, {simbolo}) = {proximo_estado}")
        estado_atual = proximo_estado
    
    # Verificar se o estado final é um estado de aceitação
    aceita = estado_atual in automato.estados_finais
    
    print("\n> Estado final alcançado: {0}".format(estado_atual))
    if aceita:
        print(f"✅ ACEITA: O estado {estado_atual} é um estado de aceitação.")
        print(f"   Estados de aceitação: {{{', '.join(str(estado) for estado in sorted(automato.estados_finais))}}}")
    else:
        print(f"❌ REJEITA: O estado {estado_atual} não é um estado de aceitação.")
        print(f"   Estados de aceitação: {{{', '.join(str(estado) for estado in sorted(automato.estados_finais))}}}")
    
    print("==========================================")
    
    return aceita

def simular_cadeia_detalhada(automato, cadeia):
    """
    Simula a execução de uma cadeia em um autômato finito com saída detalhada.
    
    Esta função fornece uma saída mais detalhada da simulação, incluindo
    informações sobre o autômato e a configuração em cada passo.
    
    Args:
        automato: AutomatoFinito a ser utilizado na simulação.
        cadeia (str): Cadeia de entrada a ser processada.
        
    Returns:
        bool: True se a cadeia for aceita, False caso contrário.
    """
    # Verificar se o autômato é determinístico
    if not automato.deterministic:
        raise ValueError("A simulação direta só é possível em autômatos determinísticos. " +
                         "Converta o autômato para AFD antes de simular.")
    
    # Inicializar o estado atual como o estado inicial do autômato
    estado_atual = automato.estado_inicial
    
    # Imprimir cabeçalho
    print("\n================================================================")
    print(f"  SIMULAÇÃO DETALHADA: {automato.nome}")
    print("================================================================")
    
    # Imprimir informações sobre o autômato
    print("\n[1] INFORMAÇÕES DO AUTÔMATO")
    print("-" * 50)
    print(f"Tipo: {'AFD' if automato.deterministic else 'AFN'} ({automato.nome})")
    print(f"Estados (Q): {{{', '.join(str(estado) for estado in sorted(automato.estados))}}}")
    print(f"Alfabeto (Σ): {{{', '.join(sorted(automato.alfabeto))}}}")
    print(f"Estado inicial (q0): {automato.estado_inicial}")
    print(f"Estados finais (F): {{{', '.join(str(estado) for estado in sorted(automato.estados_finais))}}}")
    
    # Imprimir a tabela de transições
    print("\n[2] TABELA DE TRANSIÇÕES (FUNÇÃO δ)")
    print("-" * 50)
    
    # Determinar o tamanho máximo dos estados para formatação
    max_estado_len = max(len(str(estado)) for estado in automato.estados)
    
    # Cabeçalho da tabela
    header = f"{'Estado':^{max_estado_len+2}} |"
    for simbolo in sorted(automato.alfabeto):
        header += f" {simbolo:^{max_estado_len+2}} |"
    header += " Final?"
    print(header)
    
    # Separador
    print("-" * (len(header)))
    
    # Linhas da tabela
    for estado in sorted(automato.estados, key=str):
        row = f" {estado:^{max_estado_len}} |"
        for simbolo in sorted(automato.alfabeto):
            transicao = automato.obter_transicao_afd(estado, simbolo)
            transicao_str = str(transicao) if transicao is not None else "—"
            row += f" {transicao_str:^{max_estado_len+2}} |"
        row += f" {'Sim' if estado in automato.estados_finais else 'Não':^6}"
        print(row)
    
    # Simulação passo a passo
    print("\n[3] SIMULAÇÃO DA CADEIA")
    print("-" * 50)
    
    # Verificar caso especial de cadeia vazia
    if not cadeia:
        print(f"Cadeia de entrada: '' (cadeia vazia)")
    else:
        print(f"Cadeia de entrada: '{cadeia}'")
    
    print(f"\nEstado inicial: {estado_atual}")
    
    # Histórico de configurações para a visualização final
    historico = [(estado_atual, "")]
    
    for i, simbolo in enumerate(cadeia):
        # Verificar se o símbolo pertence ao alfabeto
        if simbolo not in automato.alfabeto:
            print(f"\n❌ ERRO: O símbolo '{simbolo}' não pertence ao alfabeto do autômato.")
            print(f"   Alfabeto permitido: {{{', '.join(sorted(automato.alfabeto))}}}")
            return False
        
        # Obter o próximo estado
        proximo_estado = automato.obter_transicao_afd(estado_atual, simbolo)
        
        # Verificar se existe uma transição definida
        if proximo_estado is None:
            print(f"\n❌ ERRO: Não há transição definida para o par ({estado_atual}, {simbolo}).")
            return False
        
        print(f"Passo {i+1}: Lendo '{simbolo}' - δ({estado_atual}, {simbolo}) = {proximo_estado}")
        estado_atual = proximo_estado
        
        # Adicionar ao histórico
        simbolos_lidos = cadeia[:i+1]
        historico.append((estado_atual, simbolos_lidos))
    
    # Verificar se o estado final é um estado de aceitação
    aceita = estado_atual in automato.estados_finais
    
    # Exibir o resultado e o histórico da simulação
    print("\n[4] RESULTADO DA SIMULAÇÃO")
    print("-" * 50)
    print(f"Estado final alcançado: {estado_atual}")
    if aceita:
        print(f"✅ CADEIA ACEITA: O estado {estado_atual} é um estado de aceitação.")
    else:
        print(f"❌ CADEIA REJEITADA: O estado {estado_atual} não é um estado de aceitação.")
    
    # Histórico de configurações
    print("\n[5] HISTÓRICO DE CONFIGURAÇÕES")
    print("-" * 50)
    print(f"{'Passo':^6} | {'Símbolos Lidos':^15} | {'Estado':^8} | {'Aceitação':^10}")
    print("-" * 48)
    
    for i, (estado, simbolos) in enumerate(historico):
        simbolos_str = "ε" if not simbolos else simbolos
        aceito = "Sim" if estado in automato.estados_finais else "Não"
        print(f"{i:^6} | {simbolos_str:^15} | {estado:^8} | {aceito:^10}")
    
    print("\n================================================================")
    
    return aceita


def visualizar_tabela_transicoes(automato):
    """
    Exibe a tabela de transições do autômato de forma legível.
    
    Args:
        automato: AutomatoFinito a ser visualizado.
    """
    print(f"\n===== Tabela de Transições do {automato.nome} =====")
    
    # Determinar o tamanho máximo dos estados para formatação
    max_estado_len = max(len(str(estado)) for estado in automato.estados)
    
    # Cabeçalho da tabela
    header = f"{'Estado':^{max_estado_len+2}} |"
    for simbolo in sorted(automato.alfabeto):
        header += f" {simbolo:^{max_estado_len+2}} |"
    header += " Final?"
    print(header)
    
    # Separador
    print("-" * (len(header)))
    
    # Linhas da tabela
    for estado in sorted(automato.estados, key=str):
        row = f" {estado:^{max_estado_len}} |"
        for simbolo in sorted(automato.alfabeto):
            if automato.deterministic:
                transicao = automato.obter_transicao_afd(estado, simbolo)
                transicao_str = str(transicao) if transicao is not None else "—"
            else:
                transicao = automato.obter_transicoes_afn(estado, simbolo)
                transicao_str = str(transicao) if transicao else "—"
            row += f" {transicao_str:^{max_estado_len+2}} |"
        row += f" {'Sim' if estado in automato.estados_finais else 'Não':^6}"
        print(row)
    
    print("")