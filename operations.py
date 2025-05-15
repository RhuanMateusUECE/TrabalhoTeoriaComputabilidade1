# operations.py
"""
Módulo para operações de fechamento em Autômatos Finitos.
Implementa as operações de reverso e complemento.
"""

from automato import AutomatoFinitoDeterministico, AutomatoFinitoNaoDeterministico
from afn_to_afd import converter_afn_para_afd

def aplicar_reverso(afd):
    """
    Aplica a operação de reverso a um Autômato Finito Determinístico (AFD).
    
    O reverso de um autômato é obtido invertendo a direção de todas as transições
    e trocando o estado inicial e os estados finais.
    
    Args:
        afd: AutomatoFinitoDeterministico a ser revertido.
        
    Returns:
        AutomatoFinitoDeterministico: O AFD resultante após a operação de reverso.
    """
    # Primeiro, criamos um AFN que representa o reverso do AFD
    afn_reverso = AutomatoFinitoNaoDeterministico(
        alfabeto=afd.alfabeto.copy(),
        nome="AFN Reverso"
    )
    
    # Adicionar estados
    for estado in afd.estados:
        afn_reverso.adicionar_estado(estado)
    
    # Adicionar um novo estado inicial
    afn_reverso.adicionar_estado("q_inicial_reverso")
    afn_reverso.definir_estado_inicial("q_inicial_reverso")
    
    # Adicionar transições epsilon do novo estado inicial para os antigos estados finais
    for estado_final in afd.estados_finais:
        afn_reverso.adicionar_transicao("q_inicial_reverso", "ε", estado_final)
    
    # Inverter as transições
    for (estado_origem, simbolo), estado_destino in afd.transicoes.items():
        afn_reverso.adicionar_transicao(estado_destino, simbolo, estado_origem)
    
    # Adicionar o antigo estado inicial como estado final do AFN reverso
    afn_reverso.adicionar_estado_final(afd.estado_inicial)
    
    # Converter o AFN reverso para AFD
    afd_reverso = converter_afn_para_afd(afn_reverso)
    afd_reverso.nome = "AFD Reverso"
    
    return afd_reverso

def aplicar_complemento(afd):
    """
    Aplica a operação de complemento a um Autômato Finito Determinístico (AFD).
    
    O complemento de um autômato é obtido trocando estados finais por não-finais
    e vice-versa, mantendo as mesmas transições.
    
    Args:
        afd: AutomatoFinitoDeterministico a ser complementado.
        
    Returns:
        AutomatoFinitoDeterministico: O AFD resultante após a operação de complemento.
    """
    # Criar um novo AFD para o complemento
    afd_complemento = AutomatoFinitoDeterministico(
        alfabeto=afd.alfabeto.copy(),
        nome="AFD Complemento"
    )
    
    # Adicionar todos os estados
    for estado in afd.estados:
        afd_complemento.adicionar_estado(estado)
        
        # Se um estado não é final no AFD original, ele se torna final no complemento
        if estado not in afd.estados_finais:
            afd_complemento.adicionar_estado_final(estado)
    
    # Definir o estado inicial
    afd_complemento.definir_estado_inicial(afd.estado_inicial)
    
    # Adicionar todas as transições
    for (estado_origem, simbolo), estado_destino in afd.transicoes.items():
        afd_complemento.adicionar_transicao(estado_origem, simbolo, estado_destino)
    
    # Verificar se o AFD é completo (tem transições definidas para todos os estados e símbolos)
    afd_complemento = completar_afd(afd_complemento)
    
    return afd_complemento

def completar_afd(afd):
    """
    Completa um AFD, adicionando um estado sumidouro e as transições necessárias.
    
    Um AFD completo tem uma transição definida para cada par (estado, símbolo).
    Para completar um AFD, adicionamos um estado sumidouro e transições para ele
    quando não há uma transição definida para um par (estado, símbolo).
    
    Args:
        afd: AutomatoFinitoDeterministico a ser completado.
        
    Returns:
        AutomatoFinitoDeterministico: O AFD completado.
    """
    # Verificar se já existe algum estado sumidouro no AFD
    # (um estado não-final para o qual todas as transições levam a ele mesmo)
    estado_sumidouro = None
    
    # Verificar se todas as transições estão definidas
    transicoes_faltantes = []
    
    for estado in afd.estados:
        for simbolo in afd.alfabeto:
            chave = (estado, simbolo)
            if chave not in afd.transicoes:
                transicoes_faltantes.append(chave)
    
    # Se não há transições faltantes, o AFD já está completo
    if not transicoes_faltantes:
        return afd
    
    # Criar um novo estado sumidouro
    estado_sumidouro = "q_sumidouro"
    afd.adicionar_estado(estado_sumidouro)
    
    # Adicionar transições do estado sumidouro para ele mesmo, para todos os símbolos
    for simbolo in afd.alfabeto:
        afd.adicionar_transicao(estado_sumidouro, simbolo, estado_sumidouro)
    
    # Adicionar transições faltantes para o estado sumidouro
    for estado, simbolo in transicoes_faltantes:
        afd.adicionar_transicao(estado, simbolo, estado_sumidouro)
    
    return afd