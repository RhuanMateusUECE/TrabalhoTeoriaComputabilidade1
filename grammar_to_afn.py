#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trabalho Prático - Teoria da Computação
Implementação de Simulação de Autômato Finito com Operações e Gramática Linear à Direita

Etapa 1: Conversão Gramática → AFN
Etapa 2: Determinização AFN → AFD

Autores: [Seus nomes aqui]
Data: Maio 2025
"""


class Gramatica:
    """Classe para representar uma Gramática Linear Unitária à Direita (GLUD)"""
    
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial):
        self.V = set(nao_terminais)  # Conjunto de não-terminais
        self.T = set(terminais)      # Conjunto de terminais
        self.P = producoes           # Conjunto de produções
        self.S = simbolo_inicial     # Símbolo inicial
    
    def __str__(self):
        return f"G = (V: {self.V}, T: {self.T}, P: {self.P}, S: {self.S})"


class AFN:
    """Classe para representar um Autômato Finito Não-determinístico"""
    
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.Q = set(estados)           # Conjunto de estados
        self.sigma = set(alfabeto)      # Alfabeto de entrada
        self.delta = transicoes         # Função de transição
        self.q0 = estado_inicial        # Estado inicial
        self.F = set(estados_finais)    # Conjunto de estados finais
    
    def __str__(self):
        resultado = "# AFN Original\n"
        resultado += f"Q: {', '.join(sorted(self.Q))}\n"
        resultado += f"Σ: {', '.join(sorted(self.sigma))}\n"
        resultado += "δ:\n"
        
        # Ordenar transições para saída consistente
        for estado in sorted(self.Q):
            for simbolo in sorted(self.sigma | {'ε'}):
                if (estado, simbolo) in self.delta:
                    destinos = self.delta[(estado, simbolo)]
                    if isinstance(destinos, set):
                        for destino in sorted(destinos):
                            resultado += f"{estado}, {simbolo} -> {destino}\n"
                    else:
                        resultado += f"{estado}, {simbolo} -> {destinos}\n"
        
        resultado += f"{self.q0}: inicial\n"
        resultado += f"F: {', '.join(sorted(self.F))}\n"
        
        return resultado


class AFD:
    """Classe para representar um Autômato Finito Determinístico"""
    
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.Q = set(estados)           # Conjunto de estados
        self.sigma = set(alfabeto)      # Alfabeto de entrada
        self.delta = transicoes         # Função de transição
        self.q0 = estado_inicial        # Estado inicial
        self.F = set(estados_finais)    # Conjunto de estados finais
    
    def __str__(self):
        resultado = "# AFD Determinizado\n"
        resultado += f"Q: {', '.join(sorted(self.Q))}\n"
        resultado += f"Σ: {', '.join(sorted(self.sigma))}\n"
        resultado += "δ:\n"
        
        # Ordenar transições para saída consistente
        for estado in sorted(self.Q):
            for simbolo in sorted(self.sigma):
                if (estado, simbolo) in self.delta:
                    destino = self.delta[(estado, simbolo)]
                    resultado += f"{estado}, {simbolo} -> {destino}\n"
        
        resultado += f"{self.q0}: inicial\n"
        resultado += f"F: {', '.join(sorted(self.F))}\n"
        
        return resultado


def ler_gramatica_arquivo(nome_arquivo):
    """
    Lê uma gramática de um arquivo de texto
    
    Formato esperado:
    # Gramática: G = ({S, A}, {a, b}, P, S)
    S -> aA
    A -> bS
    S -> ε
    w = abab
    """
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        # Remover linhas vazias e comentários
        linhas = [linha.strip() for linha in linhas if linha.strip() and not linha.strip().startswith('#')]
        
        # Encontrar linha da definição da gramática (se houver)
        definicao_gramatica = None
        producoes = []
        cadeia_teste = None
        
        for linha in linhas:
            if linha.startswith('G =') or linha.startswith('# Gramática:'):
                definicao_gramatica = linha
            elif linha.startswith('w ='):
                # Cadeia de teste
                cadeia_teste = linha.split('=')[1].strip()
            elif '->' in linha:
                # Produção
                producoes.append(linha)
        
        # Extrair informações da definição da gramática (se presente)
        nao_terminais = set()
        terminais = set()
        simbolo_inicial = None
        
        if definicao_gramatica:
            # Parse da linha G = ({S, A}, {a, b}, P, S)
            try:
                # Remover "G =" e espaços
                conteudo = definicao_gramatica.replace('G =', '').replace('# Gramática:', '').strip()
                conteudo = conteudo.strip('()')
                
                # Split por vírgulas, mas cuidado com conjuntos
                partes = []
                nivel = 0
                parte_atual = ""
                
                for char in conteudo:
                    if char == '{':
                        nivel += 1
                    elif char == '}':
                        nivel -= 1
                    elif char == ',' and nivel == 0:
                        partes.append(parte_atual.strip())
                        parte_atual = ""
                        continue
                    parte_atual += char
                
                if parte_atual.strip():
                    partes.append(parte_atual.strip())
                
                # Extrair não-terminais (primeiro conjunto)
                if len(partes) >= 1:
                    nt_str = partes[0].strip('{}')
                    nao_terminais = set([nt.strip() for nt in nt_str.split(',') if nt.strip()])
                
                # Extrair terminais (segundo conjunto)
                if len(partes) >= 2:
                    t_str = partes[1].strip('{}')
                    terminais = set([t.strip() for t in t_str.split(',') if t.strip()])
                
                # Símbolo inicial (último elemento)
                if len(partes) >= 4:
                    simbolo_inicial = partes[3].strip()
                
            except:
                print("AVISO: Não foi possível parsear a definição da gramática. Inferindo dos dados...")
        
        # Se não conseguiu extrair da definição, inferir das produções
        if not nao_terminais or not terminais or not simbolo_inicial:
            print("Inferindo gramática das produções...")
            
            for producao in producoes:
                if '->' in producao:
                    esquerda, direita = producao.split('->')
                    esquerda = esquerda.strip()
                    direita = direita.strip()
                    
                    # Lado esquerdo é sempre não-terminal
                    nao_terminais.add(esquerda)
                    
                    # Analisar lado direito
                    if direita != 'ε' and direita != '':
                        for char in direita:
                            if char.isupper():
                                nao_terminais.add(char)
                            elif char.islower():
                                terminais.add(char)
            
            # Símbolo inicial é o primeiro não-terminal das produções
            if not simbolo_inicial and producoes:
                simbolo_inicial = producoes[0].split('->')[0].strip()
        
        print(f"Gramática lida do arquivo '{nome_arquivo}':")
        print(f"  Não-terminais: {nao_terminais}")
        print(f"  Terminais: {terminais}")
        print(f"  Produções: {producoes}")
        print(f"  Símbolo inicial: {simbolo_inicial}")
        if cadeia_teste:
            print(f"  Cadeia de teste: {cadeia_teste}")
        print()
        
        return Gramatica(nao_terminais, terminais, producoes, simbolo_inicial), cadeia_teste
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{nome_arquivo}' não encontrado!")
        return None, None
    except Exception as e:
        print(f"ERRO ao ler arquivo: {e}")
        return None, None


def converter_gramatica_para_afn(gramatica):
    """
    Converte uma Gramática Linear Unitária à Direita (GLUD) para um AFN
    
    Algoritmo:
    1. Q = V ∪ {Z}, onde Z é o estado final
    2. Σ = T
    3. δ = ∅
    4. q0 = S
    5. F = {Z}
    
    Para cada produção α → β:
    - X → aY: δ(X,a) → Y
    - X → Y:  δ(X,ε) → Y  
    - X → a:  δ(X,a) → Z
    - X → ε:  δ(X,ε) → Z
    """
    
    # Passo 1: Q = V ∪ {Z}
    Z = 'Z'  # Estado final especial
    while Z in gramatica.V:  # Garantir que Z não conflite com estados existentes
        Z += '_'
    
    Q = gramatica.V.copy()
    Q.add(Z)
    
    # Passo 2: Σ = T
    sigma = gramatica.T.copy()
    
    # Passo 3: δ = ∅ (inicializar função de transição vazia)
    delta = {}
    
    # Passo 4: q0 = S
    q0 = gramatica.S
    
    # Passo 5: F = {Z}
    F = {Z}
    
    # Processar cada produção P
    for producao in gramatica.P:
        lado_esquerdo, lado_direito = producao.split(' -> ')
        X = lado_esquerdo.strip()
        beta = lado_direito.strip()
        
        # Caso 1: X → aY (terminal seguido de não-terminal)
        if len(beta) == 2 and beta[0] in gramatica.T and beta[1] in gramatica.V:
            a, Y = beta[0], beta[1]
            if (X, a) not in delta:
                delta[(X, a)] = set()
            delta[(X, a)].add(Y)
            print(f"Produção {producao}: δ({X}, {a}) -> {Y}")
        
        # Caso 2: X → Y (apenas não-terminal)
        elif len(beta) == 1 and beta in gramatica.V:
            Y = beta
            if (X, 'ε') not in delta:
                delta[(X, 'ε')] = set()
            delta[(X, 'ε')].add(Y)
            print(f"Produção {producao}: δ({X}, ε) -> {Y}")
        
        # Caso 3: X → a (apenas terminal)
        elif len(beta) == 1 and beta in gramatica.T:
            a = beta
            if (X, a) not in delta:
                delta[(X, a)] = set()
            delta[(X, a)].add(Z)
            print(f"Produção {producao}: δ({X}, {a}) -> {Z}")
        
        # Caso 4: X → ε (palavra vazia)
        elif beta == 'ε' or beta == '':
            if (X, 'ε') not in delta:
                delta[(X, 'ε')] = set()
            delta[(X, 'ε')].add(Z)
            print(f"Produção {producao}: δ({X}, ε) -> {Z}")
        
        else:
            print(f"AVISO: Produção '{producao}' não reconhecida ou não é GLUD válida")
    
    return AFN(Q, sigma, delta, q0, F)


def epsilon_closure(estados, delta):
    """
    Calcula o ε-closure (fechamento epsilon) de um conjunto de estados
    
    Args:
        estados: conjunto de estados
        delta: função de transição do AFN
    
    Returns:
        conjunto de estados alcançáveis via transições ε
    """
    closure = set(estados)
    pilha = list(estados)
    
    while pilha:
        estado_atual = pilha.pop()
        
        # Verificar se existe transição ε a partir do estado atual
        if (estado_atual, 'ε') in delta:
            destinos_epsilon = delta[(estado_atual, 'ε')]
            
            # Se destinos_epsilon não é conjunto, converter
            if not isinstance(destinos_epsilon, set):
                destinos_epsilon = {destinos_epsilon}
            
            # Adicionar novos estados encontrados
            for destino in destinos_epsilon:
                if destino not in closure:
                    closure.add(destino)
                    pilha.append(destino)
    
    return closure


def converter_afn_para_afd(afn):
    """
    Converte um AFN para AFD usando o algoritmo de determinização
    
    Algoritmo:
    1. Q = P(Q1) - Conjunto potência dos estados do AFN
    2. Σ = Σ1 - Mesmo alfabeto
    3. δ(R, a) = ∪(r∈R) δ1(r, a) - União das transições
    4. q0 = ε-closure({q01}) - Estado inicial com fechamento epsilon
    5. F = {R | R ∩ F1 ≠ ∅} - Estados que contêm pelo menos um estado final do AFN
    """
    
    print("=== Iniciando Determinização AFN → AFD ===")
    
    # Passo 2: Σ = Σ1 (alfabeto sem ε)
    sigma_afd = afn.sigma.copy()
    
    # Passo 4: q0 = ε-closure({q01})
    estado_inicial_afn = {afn.q0}
    q0_afd = epsilon_closure(estado_inicial_afn, afn.delta)
    print(f"Estado inicial AFD: ε-closure({{{afn.q0}}}) = {sorted(q0_afd)}")
    
    # Inicializar estruturas para o AFD
    Q_afd = []  # Lista de estados (conjuntos de estados do AFN)
    delta_afd = {}  # Função de transição do AFD
    estados_visitados = set()  # Para evitar duplicatas
    fila_estados = []  # Fila para processamento BFS
    
    # Converter conjunto para string ordenada para usar como chave
    def conjunto_para_string(conjunto):
        if not conjunto:
            return "∅"
        return "{" + ", ".join(sorted(conjunto)) + "}"
    
    # Adicionar estado inicial à fila
    q0_str = conjunto_para_string(q0_afd)
    Q_afd.append(q0_str)
    estados_visitados.add(q0_str)
    fila_estados.append((q0_str, q0_afd))
    
    print(f"\nProcessando estados:")
    
    # Processar cada estado na fila
    while fila_estados:
        estado_str, estado_conjunto = fila_estados.pop(0)
        print(f"\nProcessando estado {estado_str}:")
        
        # Passo 3: Para cada símbolo do alfabeto
        for simbolo in sorted(sigma_afd):
            # δ(R, a) = ∪(r∈R) δ1(r, a)
            novos_estados = set()
            
            for r in estado_conjunto:
                if (r, simbolo) in afn.delta:
                    destinos = afn.delta[(r, simbolo)]
                    if isinstance(destinos, set):
                        novos_estados.update(destinos)
                    else:
                        novos_estados.add(destinos)
            
            # Aplicar ε-closure no resultado
            if novos_estados:
                novos_estados = epsilon_closure(novos_estados, afn.delta)
            
            # Converter para string
            novo_estado_str = conjunto_para_string(novos_estados)
            
            print(f"  δ({estado_str}, {simbolo}) = {novo_estado_str}")
            
            # Adicionar transição ao AFD
            delta_afd[(estado_str, simbolo)] = novo_estado_str
            
            # Se é um novo estado, adicionar à fila
            if novo_estado_str not in estados_visitados and novos_estados:
                Q_afd.append(novo_estado_str)
                estados_visitados.add(novo_estado_str)
                fila_estados.append((novo_estado_str, novos_estados))
    
    # Passo 5: F = {R | R ∩ F1 ≠ ∅}
    F_afd = set()
    
    print(f"\nDeterminando estados finais:")
    print(f"Estados finais do AFN: {sorted(afn.F)}")
    
    for estado_str in Q_afd:
        # Reconstruir conjunto a partir da string
        if estado_str == "∅":
            continue
            
        # Extrair estados do formato "{S, A, Z}"
        estado_limpo = estado_str.strip("{}")
        if estado_limpo:
            estados_no_conjunto = set([e.strip() for e in estado_limpo.split(",")])
            
            # Verificar se há interseção com estados finais do AFN
            if estados_no_conjunto.intersection(afn.F):
                F_afd.add(estado_str)
                print(f"  {estado_str} é final (contém {estados_no_conjunto.intersection(afn.F)})")
    
    print(f"\nEstados finais do AFD: {sorted(F_afd)}")
    
    # Criar AFD resultante
    return AFD(Q_afd, sigma_afd, delta_afd, q0_str, F_afd)


def salvar_afn_arquivo(afn, nome_arquivo="AFN.txt"):
    """Salva a representação do AFN em um arquivo"""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(str(afn))
    print(f"AFN salvo em {nome_arquivo}")


def salvar_afd_arquivo(afd, nome_arquivo="AFD.txt"):
    """Salva a representação do AFD em um arquivo"""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(str(afd))
    print(f"AFD salvo em {nome_arquivo}")


def criar_arquivo_exemplo():
    """Cria um arquivo de exemplo para testar"""
    conteudo = """# Gramática: G = ({S, A}, {a, b}, P, S)

S -> aA
A -> bS
S -> ε

w = abab"""
    
    with open('entrada.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(conteudo)
    
    print("Arquivo de exemplo 'entrada.txt' criado!")


def exemplo_uso():
    """Exemplo de uso da conversão Gramática → AFN → AFD"""
    
    print("=== Conversão Gramática → AFN → AFD ===\n")
    
    # Criar arquivo de exemplo se não existir
    import os
    if not os.path.exists('entrada.txt'):
        criar_arquivo_exemplo()
    
    # Etapa 1: Ler gramática do arquivo e converter para AFN
    gramatica, cadeia_teste = ler_gramatica_arquivo('entrada.txt')
    
    if gramatica is None:
        print("Erro ao ler gramática. Encerrando.")
        return None
    
    print("Etapa 1: Processando produções para AFN:")
    afn = converter_gramatica_para_afn(gramatica)
    print()
    
    print("AFN resultante:")
    print(afn)
    salvar_afn_arquivo(afn)
    print()
    
    # Etapa 2: Converter AFN para AFD
    afd = converter_afn_para_afd(afn)
    print()
    
    print("AFD resultante:")
    print(afd)
    salvar_afd_arquivo(afd)
    
    if cadeia_teste:
        print(f"\nCadeia de teste encontrada: {cadeia_teste}")
        print("(Simulação será implementada nas próximas etapas)")
    
    return afn, afd, cadeia_teste


if __name__ == "__main__":
    exemplo_uso()