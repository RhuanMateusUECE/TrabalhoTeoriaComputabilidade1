# afn_to_afd.py
"""
Módulo para conversão de um Autômato Finito Não-determinístico (AFN) 
para um Autômato Finito Determinístico (AFD).
"""

from automato import AutomatoFinitoDeterministico

def converter_afn_para_afd(afn):
    """
    Converte um Autômato Finito Não-determinístico (AFN) para um 
    Autômato Finito Determinístico (AFD) equivalente.
    
    Args:
        afn: AutomatoFinitoNaoDeterministico a ser convertido.
        
    Returns:
        AutomatoFinitoDeterministico: AFD equivalente ao AFN de entrada.
    """
    # Criar um novo AFD
    afd = AutomatoFinitoDeterministico(
        alfabeto=afn.alfabeto.copy(),
        nome="AFD Determinizado"
    )
    
    # Começar com o epsilon-fecho do estado inicial do AFN
    estado_inicial_afd = frozenset(afn.obter_epsilon_fecho(afn.estado_inicial))
    
    # Verificar se o estado inicial do AFD é um estado final
    estados_finais_afd = set()
    if any(estado in afn.estados_finais for estado in estado_inicial_afd):
        estados_finais_afd.add(estado_inicial_afd)
    
    # Inicializar estruturas para o algoritmo de determinização
    estados_afd = {estado_inicial_afd}  # Estados já criados no AFD
    estados_a_processar = [estado_inicial_afd]  # Fila de estados a serem processados
    transicoes_afd = {}  # Transições do AFD
    
    # Definir o estado inicial do AFD
    afd.definir_estado_inicial(estado_inicial_afd)
    
    # Algoritmo de determinização
    while estados_a_processar:
        estado_atual = estados_a_processar.pop(0)
        
        # Para cada símbolo do alfabeto
        for simbolo in afn.alfabeto:
            # Calcular o conjunto de estados alcançados no AFN com este símbolo
            estados_destino = set()
            for estado in estado_atual:
                estados_destino.update(afn.obter_transicoes_afn(estado, simbolo))
            
            # Calcular o epsilon-fecho dos estados destino
            epsilon_fecho_destino = set()
            for estado in estados_destino:
                epsilon_fecho_destino.update(afn.obter_epsilon_fecho(estado))
            
            # Converter para frozenset para usar como chave no dicionário
            epsilon_fecho_destino_frozen = frozenset(epsilon_fecho_destino)
            
            # Se o conjunto não for vazio, adicionar a transição
            if epsilon_fecho_destino:
                transicoes_afd[(estado_atual, simbolo)] = epsilon_fecho_destino_frozen
                
                # Se este é um novo estado, adicioná-lo à lista de estados a processar
                if epsilon_fecho_destino_frozen not in estados_afd:
                    estados_afd.add(epsilon_fecho_destino_frozen)
                    estados_a_processar.append(epsilon_fecho_destino_frozen)
                    
                    # Verificar se este novo estado deve ser um estado final
                    if any(estado in afn.estados_finais for estado in epsilon_fecho_destino_frozen):
                        estados_finais_afd.add(epsilon_fecho_destino_frozen)
    
    # Adicionar estados e transições ao AFD
    for estado in estados_afd:
        afd.adicionar_estado(estado)
    
    for (estado_origem, simbolo), estado_destino in transicoes_afd.items():
        afd.adicionar_transicao(estado_origem, simbolo, estado_destino)
    
    # Adicionar estados finais
    for estado in estados_finais_afd:
        afd.adicionar_estado_final(estado)
    
    # Renomear os estados para maior legibilidade (opcional)
    return renomear_estados_afd(afd)

def renomear_estados_afd(afd):
    """
    Renomeia os estados do AFD para maior legibilidade.
    Os estados são renomeados como q0, q1, q2, etc.
    
    Args:
        afd: AutomatoFinitoDeterministico a ter os estados renomeados.
        
    Returns:
        AutomatoFinitoDeterministico: AFD com estados renomeados.
    """
    # Criar um novo AFD com os estados renomeados
    afd_renomeado = AutomatoFinitoDeterministico(
        alfabeto=afd.alfabeto.copy(),
        nome=afd.nome
    )
    
    # Mapear estados originais para novos nomes
    mapeamento_estados = {}
    
    # Garantir que o estado inicial seja q0
    mapeamento_estados[afd.estado_inicial] = "q0"
    
    # Atribuir nomes para os demais estados
    contador = 1
    for estado in afd.estados:
        if estado != afd.estado_inicial:
            mapeamento_estados[estado] = f"q{contador}"
            contador += 1
    
    # Adicionar estados ao novo AFD
    for estado in afd.estados:
        novo_nome = mapeamento_estados[estado]
        afd_renomeado.adicionar_estado(novo_nome)
        
        # Verificar se é estado final
        if estado in afd.estados_finais:
            afd_renomeado.adicionar_estado_final(novo_nome)
    
    # Definir o estado inicial
    afd_renomeado.definir_estado_inicial(mapeamento_estados[afd.estado_inicial])
    
    # Adicionar transições
    for (estado_origem, simbolo), estado_destino in afd.transicoes.items():
        origem_renomeada = mapeamento_estados[estado_origem]
        destino_renomeada = mapeamento_estados[estado_destino]
        afd_renomeado.adicionar_transicao(origem_renomeada, simbolo, destino_renomeada)
    
    return afd_renomeado