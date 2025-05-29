#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trabalho Prático - Teoria da Computação
Implementação de Simulação de Autômato Finito com Operações e Gramática Linear à Direita

Etapa 1: Conversão Gramática → AFN
Etapa 2: Determinização AFN → AFD
Etapa 3: Operações de Fechamento (Reverso e Complemento)
Etapa 4: Simulação de cadeia de entrada
Etapa 5: Geração de arquivos de saída

Professor: Bonfim Amaro Junior
Disciplina: Teoria da Computação
Data de Entrega: 05/06/2025

Autores: Rhuan Mateus Matias Filgueira e Hilbert
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


def normalizar_afd_um_estado_final(afd):
    """
    1ª parte: Converte AFD com |F| > 1 em AFD' com |F| = 1
    
    ENTRADA: AF (Q, Σ, δ, q0, F) | |F| > 1 
    SAÍDA: AF' (Q', Σ', δ', q0', F') | |F'| = 1
    
    Procedimento:
    1. Q' = Q ∪ {qf'}
    2. Σ' = Σ  
    3. δ'(q,a) = {
           δ(q,a) | q ∈ Q - F
           δ(q,a) | q ∈ F e a != ε
           δ(q,a) ∪ {qf'} | q ∈ F e a = ε
       }
    4. q0' = q0
    5. F' = {qf'}
    """
    
    print("=== Normalizando AFD para ter apenas 1 estado final ===")
    
    # Se já tem apenas 1 estado final, não precisa normalizar
    if len(afd.F) <= 1:
        print("AFD já possui apenas 1 estado final. Não necessária normalização.")
        return afd
    
    print(f"AFD possui {len(afd.F)} estados finais: {sorted(afd.F)}")
    print("Aplicando normalização...")
    
    # 1. Q' = Q ∪ {qf'}
    qf_novo = "qf'"
    while qf_novo in afd.Q:  # Garantir que não há conflito
        qf_novo += "'"
    
    Q_novo = afd.Q.copy()
    Q_novo.add(qf_novo)
    
    # 2. Σ' = Σ
    sigma_novo = afd.sigma.copy()
    
    # 3. Construir δ'
    delta_novo = {}
    
    for (estado, simbolo), destino in afd.delta.items():
        if estado not in afd.F:
            # q ∈ Q - F: δ'(q,a) = δ(q,a)
            delta_novo[(estado, simbolo)] = destino
        else:
            # q ∈ F
            if simbolo != 'ε':
                # a != ε: δ'(q,a) = δ(q,a)
                delta_novo[(estado, simbolo)] = destino
            else:
                # a = ε: δ'(q,a) = δ(q,a) ∪ {qf'}
                if isinstance(destino, set):
                    novo_destino = destino.copy()
                    novo_destino.add(qf_novo)
                else:
                    novo_destino = {destino, qf_novo}
                delta_novo[(estado, simbolo)] = novo_destino
    
    # Adicionar transições ε dos estados finais originais para o novo estado final
    for estado_final in afd.F:
        if (estado_final, 'ε') not in delta_novo:
            delta_novo[(estado_final, 'ε')] = qf_novo
        else:
            # Se já existe transição ε, adicionar qf_novo ao destino
            destino_atual = delta_novo[(estado_final, 'ε')]
            if isinstance(destino_atual, set):
                destino_atual.add(qf_novo)
            else:
                delta_novo[(estado_final, 'ε')] = {destino_atual, qf_novo}
    
    # 4. q0' = q0
    q0_novo = afd.q0
    
    # 5. F' = {qf'}
    F_novo = {qf_novo}
    
    print(f"Novo estado final criado: {qf_novo}")
    print(f"Estados finais antigos ({sorted(afd.F)}) agora têm transições ε para {qf_novo}")
    
    return AFD(Q_novo, sigma_novo, delta_novo, q0_novo, F_novo)


def reverter_automato(afd):
    """
    2ª parte: Converte AFD com |F| = 1 em AFD'' tal que L(AFD'') = L(AFD)^R
    
    ENTRADA: AF' (Q', Σ', δ', q0', {qf'}) | L(AF') = L1
    SAÍDA: AF'' (Q'', Σ'', δ'', q0'', F'') | L(AF'') = L1^R
    
    Procedimento:
    1. Q'' = Q'
    2. Σ'' = Σ'
    3. δ'' = ∅, para todas as transições δ'(qi, a) -> qj:
       δ'' = δ'' ∪ {(qj, a) -> qi}
    4. q0'' = qf' (único estado final vira inicial)
    5. F'' = {q0'} (estado inicial vira final)
    """
    
    print("=== Aplicando Operação de Reverso ===")
    
    # Verificar se tem apenas 1 estado final
    if len(afd.F) != 1:
        raise ValueError(f"AFD deve ter exatamente 1 estado final, mas tem {len(afd.F)}")
    
    # 1. Q'' = Q'
    Q_reverso = afd.Q.copy()
    
    # 2. Σ'' = Σ'
    sigma_reverso = afd.sigma.copy()
    
    # 3. Reverter todas as transições
    delta_reverso = {}
    
    print("Revertendo transições:")
    for (qi, simbolo), qj in afd.delta.items():
        # Para cada transição δ'(qi, a) -> qj
        # Criar transição reversa δ''(qj, a) -> qi
        
        if isinstance(qj, set):
            # Se qj é um conjunto, criar transição reversa para cada elemento
            for destino in qj:
                if (destino, simbolo) not in delta_reverso:
                    delta_reverso[(destino, simbolo)] = set()
                delta_reverso[(destino, simbolo)].add(qi)
                print(f"  δ({qi}, {simbolo}) -> {destino} ⟹ δ'({destino}, {simbolo}) -> {qi}")
        else:
            # qj é um único estado
            if (qj, simbolo) not in delta_reverso:
                delta_reverso[(qj, simbolo)] = set()
            delta_reverso[(qj, simbolo)].add(qi)
            print(f"  δ({qi}, {simbolo}) -> {qj} ⟹ δ'({qj}, {simbolo}) -> {qi}")
    
    # 4. q0'' = qf' (único estado final do AFD original)
    q0_reverso = list(afd.F)[0]  # Pegar o único estado final
    
    # 5. F'' = {q0'} (estado inicial do AFD original)
    F_reverso = {afd.q0}
    
    print(f"\nEstado inicial do reverso: {q0_reverso} (era final no original)")
    print(f"Estado final do reverso: {F_reverso} (era inicial no original)")
    
    return AFN(Q_reverso, sigma_reverso, delta_reverso, q0_reverso, F_reverso)


def aplicar_operacao_reverso(afd):
    """
    Aplica a operação completa de reverso em um AFD
    
    Se |F| > 1: aplica normalização + reverso
    Se |F| = 1: aplica apenas reverso
    """
    
    print("=== Operação de Fechamento: REVERSO ===\n")
    
    # Verificar quantos estados finais o AFD possui
    print(f"AFD de entrada possui {len(afd.F)} estado(s) final(is): {sorted(afd.F)}")
    
    # Parte 1: Normalizar se necessário (|F| > 1)
    if len(afd.F) > 1:
        print("\n|F| > 1, aplicando normalização primeiro...")
        afd_normalizado = normalizar_afd_um_estado_final(afd)
        print(f"\nAFD normalizado:")
        print(afd_normalizado)
    else:
        print("\n|F| = 1, pulando normalização...")
        afd_normalizado = afd
    
    # Parte 2: Aplicar reverso
    print(f"\nAplicando reverso no AFD...")
    afn_reverso = reverter_automato(afd_normalizado)
    
    return afn_reverso


def salvar_reverso_arquivo(afn_reverso, nome_arquivo="REV.txt"):
    """Salva a representação do AFN reverso em um arquivo"""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        # Modificar o cabeçalho para indicar que é reverso
        conteudo = str(afn_reverso).replace("# AFN Original", "# AFD Reverso")
        arquivo.write(conteudo)
    print(f"AFD Reverso salvo em {nome_arquivo}")


def aplicar_operacao_complemento(afd):
    """
    Aplica a operação de fechamento do Complemento em um AFD
    
    ENTRADA: AFD1 (L1) => (Q1, Σ1, δ1, q01, F1)
    SAÍDA: AFD (complemento de L1) => (Q, Σ, δ, q0, F)
    
    Procedimento:
    1. Q = Q1
    2. Σ = Σ1  
    3. δ = δ1
    4. q0 = q01
    5. F = Q - F1 (estados não-finais viram finais)
    """
    
    print("=== Operação de Fechamento: COMPLEMENTO ===\n")
    
    print(f"AFD original:")
    print(f"  Estados: {sorted(afd.Q)}")
    print(f"  Estados finais: {sorted(afd.F)}")
    print(f"  Estados não-finais: {sorted(afd.Q - afd.F)}")
    
    # 1. Q = Q1 (mesmo conjunto de estados)
    Q_comp = afd.Q.copy()
    
    # 2. Σ = Σ1 (mesmo alfabeto)
    sigma_comp = afd.sigma.copy()
    
    # 3. δ = δ1 (mesma função de transição)
    delta_comp = afd.delta.copy()
    
    # 4. q0 = q01 (mesmo estado inicial)
    q0_comp = afd.q0
    
    # 5. F = Q - F1 (complemento dos estados finais)
    F_comp = afd.Q - afd.F
    
    print(f"\nAFD complemento:")
    print(f"  Estados: {sorted(Q_comp)} (inalterado)")
    print(f"  Estados finais: {sorted(F_comp)} (eram não-finais)")
    print(f"  Estados não-finais: {sorted(afd.F)} (eram finais)")
    
    print(f"\nMudança realizada:")
    print(f"  Finais antigos {sorted(afd.F)} → agora não-finais")
    print(f"  Não-finais antigos {sorted(afd.Q - afd.F)} → agora finais")
    
    return AFD(Q_comp, sigma_comp, delta_comp, q0_comp, F_comp)


def salvar_complemento_arquivo(afd_comp, nome_arquivo="COMP.txt"):
    """Salva a representação do AFD complemento em um arquivo"""
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        # Modificar o cabeçalho para indicar que é complemento
        conteudo = str(afd_comp).replace("# AFD Determinizado", "# AFD Complemento")
        arquivo.write(conteudo)
    print(f"AFD Complemento salvo em {nome_arquivo}")


def simular_cadeia_afd(afd, cadeia):
    """
    Simula a execução de uma cadeia de entrada em um AFD
    
    Args:
        afd: Autômato Finito Determinístico
        cadeia: String a ser testada
    
    Returns:
        tuple: (aceita, caminho_estados, detalhes_execucao)
    """
    
    print(f"=== Simulação da Cadeia: '{cadeia}' ===\n")
    
    if cadeia is None or cadeia == '':
        cadeia = 'ε'  # String vazia
    
    # Estado atual da simulação
    estado_atual = afd.q0
    caminho_estados = [estado_atual]
    detalhes_execucao = []
    
    print(f"Cadeia de entrada: {cadeia}")
    print(f"Estado inicial: {estado_atual}")
    print(f"Estados finais: {sorted(afd.F)}")
    print()
    
    # Processar cada símbolo da cadeia
    if cadeia == 'ε':
        # String vazia - verificar se estado inicial é final
        print("Processando string vazia (ε)")
        detalhes_execucao.append(f"String vazia - Estado atual: {estado_atual}")
    else:
        print("Processando símbolos:")
        for i, simbolo in enumerate(cadeia):
            print(f"  Passo {i+1}: δ({estado_atual}, '{simbolo}') = ", end="")
            
            # Verificar se existe transição
            if (estado_atual, simbolo) in afd.delta:
                proximo_estado = afd.delta[(estado_atual, simbolo)]
                
                # Se retorna conjunto (AFN), pegar um elemento (não deveria acontecer em AFD)
                if isinstance(proximo_estado, set):
                    if len(proximo_estado) == 1:
                        proximo_estado = list(proximo_estado)[0]
                    else:
                        print(f"ERRO: AFD retornou múltiplos estados: {proximo_estado}")
                        return False, caminho_estados, detalhes_execucao
                
                print(f"{proximo_estado}")
                
                # Atualizar estado e caminho
                estado_atual = proximo_estado
                caminho_estados.append(estado_atual)
                detalhes_execucao.append(f"δ({caminho_estados[i]}, '{simbolo}') → {estado_atual}")
                
            else:
                # Não existe transição - cadeia rejeitada
                print("INDEFINIDO (não existe transição)")
                detalhes_execucao.append(f"δ({estado_atual}, '{simbolo}') → INDEFINIDO")
                print(f"\n❌ CADEIA REJEITADA: Não existe transição de '{estado_atual}' com símbolo '{simbolo}'")
                return False, caminho_estados, detalhes_execucao
    
    # Verificar se estado final é de aceitação
    aceita = estado_atual in afd.F
    
    print(f"\nEstado final alcançado: {estado_atual}")
    print(f"Caminho percorrido: {' → '.join(caminho_estados)}")
    
    if aceita:
        print(f"✅ CADEIA ACEITA: Estado '{estado_atual}' está em F = {sorted(afd.F)}")
    else:
        print(f"❌ CADEIA REJEITADA: Estado '{estado_atual}' NÃO está em F = {sorted(afd.F)}")
    
    return aceita, caminho_estados, detalhes_execucao


def simular_cadeia_afn(afn, cadeia):
    """
    Simula a execução de uma cadeia de entrada em um AFN (para o reverso)
    Usa busca em largura para explorar todos os caminhos possíveis
    """
    
    print(f"=== Simulação da Cadeia no AFN: '{cadeia}' ===\n")
    
    if cadeia is None or cadeia == '':
        cadeia = 'ε'
    
    print(f"Cadeia de entrada: {cadeia}")
    print(f"Estado inicial: {afn.q0}")
    print(f"Estados finais: {sorted(afn.F)}")
    print()
    
    # Para AFN, usamos conjunto de estados ativos
    estados_atuais = {afn.q0}
    
    # Aplicar ε-closure no estado inicial
    estados_atuais = epsilon_closure(estados_atuais, afn.delta)
    print(f"Estados iniciais (com ε-closure): {sorted(estados_atuais)}")
    
    if cadeia == 'ε':
        # String vazia
        aceita = bool(estados_atuais.intersection(afn.F))
        print(f"String vazia - Estados finais alcançados: {sorted(estados_atuais.intersection(afn.F))}")
    else:
        # Processar cada símbolo
        for i, simbolo in enumerate(cadeia):
            print(f"\nPasso {i+1}: Processando símbolo '{simbolo}'")
            print(f"  Estados atuais: {sorted(estados_atuais)}")
            
            novos_estados = set()
            
            # Para cada estado atual, verificar transições
            for estado in estados_atuais:
                if (estado, simbolo) in afn.delta:
                    destinos = afn.delta[(estado, simbolo)]
                    if isinstance(destinos, set):
                        novos_estados.update(destinos)
                    else:
                        novos_estados.add(destinos)
                    print(f"    δ({estado}, '{simbolo}') → {destinos}")
            
            # Aplicar ε-closure
            if novos_estados:
                estados_atuais = epsilon_closure(novos_estados, afn.delta)
                print(f"  Novos estados (com ε-closure): {sorted(estados_atuais)}")
            else:
                print(f"  Nenhuma transição encontrada - AFN travado")
                estados_atuais = set()
                break
    
    # Verificar aceitação
    estados_finais_alcancados = estados_atuais.intersection(afn.F)
    aceita = len(estados_finais_alcancados) > 0
    
    print(f"\nEstados finais alcançados: {sorted(estados_finais_alcancados)}")
    
    if aceita:
        print(f"✅ CADEIA ACEITA pelo AFN")
    else:
        print(f"❌ CADEIA REJEITADA pelo AFN")
    
    return aceita


def exemplo_uso():
    """Exemplo completo: Gramática → AFN → AFD → Operações → Simulação"""
    
    print("=== TRABALHO COMPLETO: Todas as Etapas ===\n")
    
    # Criar arquivo de exemplo se não existir
    import os
    if not os.path.exists('entrada.txt'):
        criar_arquivo_exemplo()
    
    # Etapa 1: Ler gramática do arquivo e converter para AFN
    gramatica, cadeia_teste = ler_gramatica_arquivo('entrada.txt')
    
    if gramatica is None:
        print("Erro ao ler gramática. Encerrando.")
        return None
    
    print("ETAPA 1: Conversão Gramática → AFN")
    print("=" * 40)
    afn = converter_gramatica_para_afn(gramatica)
    print()
    print("AFN resultante:")
    print(afn)
    salvar_afn_arquivo(afn)
    print()
    
    # Etapa 2: Converter AFN para AFD
    print("ETAPA 2: Determinização AFN → AFD")  
    print("=" * 40)
    afd = converter_afn_para_afd(afn)
    print()
    print("AFD resultante:")
    print(afd)
    salvar_afd_arquivo(afd)
    print()
    
    # Etapa 3A: Aplicar operação de Reverso
    print("ETAPA 3A: Operação de Fechamento - REVERSO")
    print("=" * 50)
    afn_reverso = aplicar_operacao_reverso(afd)
    print()
    print("AFD Reverso resultante:")
    print(afn_reverso)
    salvar_reverso_arquivo(afn_reverso)
    print()
    
    # Etapa 3B: Aplicar operação de Complemento
    print("ETAPA 3B: Operação de Fechamento - COMPLEMENTO")
    print("=" * 55)
    afd_complemento = aplicar_operacao_complemento(afd)
    print()
    print("AFD Complemento resultante:")
    print(afd_complemento)
    salvar_complemento_arquivo(afd_complemento)
    print()
    
    # Etapa 4: Simulação da cadeia
    print("ETAPA 4: Simulação da Cadeia de Entrada")
    print("=" * 45)
    
    if cadeia_teste:
        print(f"\n🔍 Testando cadeia: '{cadeia_teste}'\n")
        
        # Simular no AFD original
        print("1️⃣ Simulação no AFD Original:")
        print("-" * 35)
        aceita_original, caminho, detalhes = simular_cadeia_afd(afd, cadeia_teste)
        
        print(f"\n2️⃣ Simulação no AFD Complemento:")
        print("-" * 38)
        aceita_complemento, _, _ = simular_cadeia_afd(afd_complemento, cadeia_teste)
        
        print(f"\n3️⃣ Simulação no AFD Reverso:")
        print("-" * 35)
        # Para o reverso, testar a cadeia invertida
        cadeia_invertida = cadeia_teste[::-1] if cadeia_teste != 'ε' else 'ε'
        print(f"Testando cadeia invertida: '{cadeia_invertida}'")
        aceita_reverso = simular_cadeia_afn(afn_reverso, cadeia_invertida)
        
        # Resumo final
        print(f"\n" + "=" * 60)
        print(f"📊 RESUMO DA SIMULAÇÃO")
        print(f"=" * 60)
        print(f"Cadeia testada: '{cadeia_teste}'")
        print(f"AFD Original:    {'✅ ACEITA' if aceita_original else '❌ REJEITA'}")
        print(f"AFD Complemento: {'✅ ACEITA' if aceita_complemento else '❌ REJEITA'}")
        print(f"AFD Reverso:     {'✅ ACEITA' if aceita_reverso else '❌ REJEITA'} (cadeia '{cadeia_invertida}')")
        
        # Verificação de consistência
        print(f"\n🔍 Verificação de Consistência:")
        if aceita_original != aceita_complemento:
            print("✅ Complemento correto: resultados opostos")
        else:
            print("⚠️  ATENÇÃO: Complemento deveria ter resultado oposto!")
            
    else:
        print("⚠️ Nenhuma cadeia de teste encontrada no arquivo de entrada.")
        print("Adicione uma linha 'w = sua_cadeia' ao arquivo entrada.txt")
    
    print(f"\n" + "=" * 60)
    print(f"📁 ARQUIVOS GERADOS:")
    print(f"=" * 60) 
    print(f"✅ AFN.txt - Autômato Finito Não-determinístico")
    print(f"✅ AFD.txt - Autômato Finito Determinístico") 
    print(f"✅ REV.txt - AFD após operação de Reverso")
    print(f"✅ COMP.txt - AFD após operação de Complemento")
    print(f"\n🎉 TRABALHO COMPLETO - TODAS AS ETAPAS IMPLEMENTADAS!")
    
    return afn, afd, afn_reverso, afd_complemento, cadeia_teste


if __name__ == "__main__":
    exemplo_uso()
