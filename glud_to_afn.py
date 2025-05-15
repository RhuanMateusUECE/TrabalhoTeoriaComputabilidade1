# glud_to_afn.py
"""
Módulo para conversão de uma Gramática Linear Unitária à Direita (GLUD)
para um Autômato Finito Não-determinístico (AFN).
"""

import re
from automato import AutomatoFinitoNaoDeterministico

def converter_glud_para_afn(arquivo_gramatica):
    """
    Converte uma Gramática Linear Unitária à Direita (GLUD) para um AFN.
    
    Args:
        arquivo_gramatica (str): Caminho do arquivo contendo a definição da gramática.
        
    Returns:
        AutomatoFinitoNaoDeterministico: AFN equivalente à gramática de entrada.
    """
    # Ler o arquivo da gramática
    gramatica = ler_arquivo_gramatica(arquivo_gramatica)
    
    # Extrair os componentes da gramática
    variaveis, terminais, producoes, simbolo_inicial = extrair_componentes_gramatica(gramatica)
    
    # Criar o AFN
    afn = criar_afn_da_gramatica(variaveis, terminais, producoes, simbolo_inicial)
    
    return afn

def ler_arquivo_gramatica(arquivo_gramatica):
    """
    Lê o arquivo da gramática e retorna suas linhas.
    
    Args:
        arquivo_gramatica (str): Caminho do arquivo contendo a definição da gramática.
        
    Returns:
        list: Lista com as linhas do arquivo da gramática.
    """
    with open(arquivo_gramatica, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
    
    # Filtrar linhas vazias e comentários
    linhas_validas = []
    for linha in linhas:
        linha = linha.strip()
        if linha and not linha.startswith('#'):
            linhas_validas.append(linha)
    
    return linhas_validas

def extrair_componentes_gramatica(linhas_gramatica):
    """
    Extrai os componentes da gramática a partir das linhas do arquivo.
    
    Args:
        linhas_gramatica (list): Lista com as linhas do arquivo da gramática.
        
    Returns:
        tuple: (variaveis, terminais, producoes, simbolo_inicial)
    """
    variaveis = set()
    terminais = set()
    producoes = []
    simbolo_inicial = None
    
    # Expressão regular para extrair produções do tipo A -> aB ou A -> a ou A -> ε
    padrao_producao = re.compile(r'([A-Z])\s*->\s*([a-z]?)([A-Z]?|\s*ε)')
    
    for linha in linhas_gramatica:
        match = padrao_producao.match(linha)
        if match:
            var_esquerda = match.group(1)
            terminal = match.group(2) if match.group(2) else ""
            var_direita = match.group(3) if match.group(3) and match.group(3) != "ε" else ""
            
            # Adicionar à lista de variáveis
            variaveis.add(var_esquerda)
            if var_direita:
                variaveis.add(var_direita)
            
            # Adicionar à lista de terminais
            if terminal:
                terminais.add(terminal)
            
            # Adicionar à lista de produções
            producoes.append((var_esquerda, terminal, var_direita))
            
            # Definir o símbolo inicial (primeira variável encontrada)
            if simbolo_inicial is None:
                simbolo_inicial = var_esquerda
    
    # Verificar se encontrou o símbolo inicial
    if simbolo_inicial is None:
        raise ValueError("Não foi possível identificar o símbolo inicial da gramática.")
    
    return variaveis, terminais, producoes, simbolo_inicial

def criar_afn_da_gramatica(variaveis, terminais, producoes, simbolo_inicial):
    """
    Cria um AFN equivalente à gramática de entrada.
    
    Algoritmo:
    1. Para cada variável da gramática, crie um estado no autômato.
    2. Adicione um estado final qf.
    3. O estado inicial do autômato é o estado correspondente ao símbolo inicial da gramática.
    4. Para cada produção A -> aB, adicione uma transição do estado A para o estado B com símbolo a.
    5. Para cada produção A -> a, adicione uma transição do estado A para o estado final qf com símbolo a.
    6. Para cada produção A -> ε, adicione o estado A aos estados finais.
    
    Args:
        variaveis (set): Conjunto de variáveis da gramática.
        terminais (set): Conjunto de terminais da gramática.
        producoes (list): Lista de produções no formato (var_esquerda, terminal, var_direita).
        simbolo_inicial (str): Símbolo inicial da gramática.
        
    Returns:
        AutomatoFinitoNaoDeterministico: AFN equivalente à gramática.
    """
    # Criar o AFN
    afn = AutomatoFinitoNaoDeterministico(nome="AFN Original")
    
    # Adicionar estados para cada variável
    for variavel in variaveis:
        afn.adicionar_estado(variavel)
    
    # Adicionar estado final qf
    afn.adicionar_estado("qf")
    afn.adicionar_estado_final("qf")
    
    # Definir estado inicial
    afn.definir_estado_inicial(simbolo_inicial)
    
    # Adicionar alfabeto
    for terminal in terminais:
        afn.adicionar_simbolo(terminal)
    
    # Adicionar transições
    for var_esquerda, terminal, var_direita in producoes:
        if terminal and var_direita:
            # Produção do tipo A -> aB
            afn.adicionar_transicao(var_esquerda, terminal, var_direita)
        elif terminal:
            # Produção do tipo A -> a
            afn.adicionar_transicao(var_esquerda, terminal, "qf")
        else:
            # Produção do tipo A -> ε
            afn.adicionar_estado_final(var_esquerda)
    
    return afn