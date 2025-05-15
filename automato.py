# automato.py
"""
Módulo para representação de Autômatos Finitos.
Define as classes e estruturas de dados para trabalhar com autômatos finitos.
"""

class AutomatoFinito:
    """
    Classe base para representação de autômatos finitos.
    Pode representar tanto Autômatos Finitos Determinísticos (AFD) quanto
    Não-Determinísticos (AFN).
    """
    
    def __init__(self, estados=None, alfabeto=None, transicoes=None, 
                 estado_inicial=None, estados_finais=None, 
                 nome="Autômato Finito"):
        """
        Inicializa um autômato finito.
        
        Args:
            estados (set): Conjunto de estados do autômato.
            alfabeto (set): Conjunto de símbolos do alfabeto.
            transicoes (dict): Dicionário de transições.
                Para AFN: {(estado, simbolo): {conjunto de estados destino}}
                Para AFD: {(estado, simbolo): estado_destino}
            estado_inicial: Estado inicial do autômato.
            estados_finais (set): Conjunto de estados finais/de aceitação.
            nome (str): Nome descritivo do autômato.
        """
        self.estados = set() if estados is None else estados
        self.alfabeto = set() if alfabeto is None else alfabeto
        self.transicoes = {} if transicoes is None else transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = set() if estados_finais is None else estados_finais
        self.nome = nome
        self.deterministic = None  # Será definido pelos métodos de criação específicos
    
    def adicionar_estado(self, estado):
        """Adiciona um estado ao autômato."""
        self.estados.add(estado)
    
    def adicionar_simbolo(self, simbolo):
        """Adiciona um símbolo ao alfabeto."""
        self.alfabeto.add(simbolo)
    
    def definir_estado_inicial(self, estado):
        """Define o estado inicial do autômato."""
        if estado not in self.estados:
            self.adicionar_estado(estado)
        self.estado_inicial = estado
    
    def adicionar_estado_final(self, estado):
        """Adiciona um estado final/de aceitação ao autômato."""
        if estado not in self.estados:
            self.adicionar_estado(estado)
        self.estados_finais.add(estado)
    
    def adicionar_transicao_afn(self, estado_origem, simbolo, estado_destino):
        """
        Adiciona uma transição para um AFN.
        
        Args:
            estado_origem: Estado de origem da transição.
            simbolo: Símbolo do alfabeto que ativa a transição.
            estado_destino: Estado destino da transição.
        """
        # Garantir que os estados e o símbolo existam no autômato
        if estado_origem not in self.estados:
            self.adicionar_estado(estado_origem)
        if estado_destino not in self.estados:
            self.adicionar_estado(estado_destino)
        if simbolo not in self.alfabeto and simbolo != "ε":  # ε representa a palavra vazia
            self.adicionar_simbolo(simbolo)
        
        # Adicionar a transição
        chave = (estado_origem, simbolo)
        if chave not in self.transicoes:
            self.transicoes[chave] = set()
        self.transicoes[chave].add(estado_destino)
        
        # Marcar o autômato como não-determinístico
        self.deterministic = False
    
    def adicionar_transicao_afd(self, estado_origem, simbolo, estado_destino):
        """
        Adiciona uma transição para um AFD.
        
        Args:
            estado_origem: Estado de origem da transição.
            simbolo: Símbolo do alfabeto que ativa a transição.
            estado_destino: Estado destino da transição.
        """
        # Garantir que os estados e o símbolo existam no autômato
        if estado_origem not in self.estados:
            self.adicionar_estado(estado_origem)
        if estado_destino not in self.estados:
            self.adicionar_estado(estado_destino)
        if simbolo not in self.alfabeto:
            self.adicionar_simbolo(simbolo)
        
        # Verificar se já existe uma transição para o mesmo par (estado, símbolo)
        chave = (estado_origem, simbolo)
        if chave in self.transicoes:
            raise ValueError(f"Transição para ({estado_origem}, {simbolo}) já definida. " +
                            "Um AFD não pode ter múltiplas transições para o mesmo par (estado, símbolo).")
        
        # Adicionar a transição
        self.transicoes[chave] = estado_destino
        
        # Marcar o autômato como determinístico
        self.deterministic = True
    
    def obter_transicoes_afn(self, estado, simbolo):
        """
        Obtém os estados destino para uma transição específica em um AFN.
        
        Args:
            estado: Estado de origem.
            simbolo: Símbolo da transição.
            
        Returns:
            set: Conjunto de estados destino.
        """
        chave = (estado, simbolo)
        return self.transicoes.get(chave, set())
    
    def obter_transicao_afd(self, estado, simbolo):
        """
        Obtém o estado destino para uma transição específica em um AFD.
        
        Args:
            estado: Estado de origem.
            simbolo: Símbolo da transição.
            
        Returns:
            O estado destino ou None se não houver transição.
        """
        chave = (estado, simbolo)
        return self.transicoes.get(chave)
    
    def obter_representacao_texto(self):
        """
        Gera uma representação textual do autômato para salvar em arquivo.
        
        Returns:
            str: Representação do autômato no formato especificado.
        """
        linhas = []
        
        # Cabeçalho com o nome do autômato
        linhas.append(f"# {self.nome}")
        
        # Conjunto de estados (Q)
        estados_str = ", ".join(str(estado) for estado in sorted(self.estados, key=str))
        linhas.append(f"Q: {estados_str}")
        
        # Alfabeto (Σ)
        alfabeto_str = ", ".join(sorted(self.alfabeto))
        linhas.append(f"Σ: {alfabeto_str}")
        
        # Função de transição (δ)
        linhas.append("δ:")
        
        # Ordenar as transições para melhor legibilidade
        chaves_ordenadas = sorted(self.transicoes.keys(), key=lambda x: (str(x[0]), x[1]))
        
        for chave in chaves_ordenadas:
            estado_origem, simbolo = chave
            destino = self.transicoes[chave]
            
            if self.deterministic:
                # AFD: uma única transição para cada par (estado, símbolo)
                linhas.append(f"{estado_origem}, {simbolo} -> {destino}")
            else:
                # AFN: múltiplas transições possíveis
                if isinstance(destino, set):
                    destinos_str = ", ".join(str(estado) for estado in sorted(destino, key=str))
                    linhas.append(f"{estado_origem}, {simbolo} -> {{{destinos_str}}}")
                else:
                    linhas.append(f"{estado_origem}, {simbolo} -> {destino}")
        
        # Estado inicial
        linhas.append(f"q0: {self.estado_inicial}")
        
        # Estados finais (F)
        finais_str = ", ".join(str(estado) for estado in sorted(self.estados_finais, key=str))
        linhas.append(f"F: {finais_str}")
        
        return "\n".join(linhas)
    
    def obter_tabela_transicoes(self):
        """
        Retorna uma representação em tabela das transições do autômato.
        
        Returns:
            str: Representação em formato de tabela.
        """
        linhas = []
        
        # Determinar o tamanho máximo dos estados para formatação
        max_estado_len = max(len(str(estado)) for estado in self.estados)
        
        # Cabeçalho da tabela
        header = f"| {'Estado':^{max_estado_len}} |"
        for simbolo in sorted(self.alfabeto):
            header += f" {simbolo:^{max_estado_len}} |"
        header += " Final? |"
        linhas.append(header)
        
        # Separador
        separador = f"|{'-' * (max_estado_len + 2)}|"
        for _ in self.alfabeto:
            separador += f"{'-' * (max_estado_len + 2)}|"
        separador += f"{'-' * 9}|"
        linhas.append(separador)
        
        # Linhas da tabela
        for estado in sorted(self.estados, key=str):
            row = f"| {estado:^{max_estado_len}} |"
            for simbolo in sorted(self.alfabeto):
                if self.deterministic:
                    transicao = self.obter_transicao_afd(estado, simbolo)
                    transicao_str = str(transicao) if transicao is not None else "—"
                else:
                    transicao = self.obter_transicoes_afn(estado, simbolo)
                    if transicao:
                        destinos = sorted(transicao, key=str)
                        transicao_str = ",".join(str(dest) for dest in destinos)
                    else:
                        transicao_str = "—"
                row += f" {transicao_str:^{max_estado_len}} |"
            
            final = "Sim" if estado in self.estados_finais else "Não"
            row += f" {final:^7} |"
            linhas.append(row)
        
        return "\n".join(linhas)
    
    def __str__(self):
        """Representação em string do autômato."""
        tipo = "Determinístico" if self.deterministic else "Não-Determinístico"
        cabecalho = f"Autômato Finito {tipo}: {self.nome}\n"
        
        # Informações básicas
        info = f"Estados: {len(self.estados)}, Símbolos: {len(self.alfabeto)}, Transições: {len(self.transicoes)}"
        
        # Tabela de transições
        tabela = self.obter_tabela_transicoes()
        
        return cabecalho + info + "\n\n" + tabela


class AutomatoFinitoDeterministico(AutomatoFinito):
    """
    Classe para representação específica de Autômatos Finitos Determinísticos (AFD).
    Herda da classe AutomatoFinito e adiciona funcionalidades específicas de AFDs.
    """
    
    def __init__(self, estados=None, alfabeto=None, transicoes=None, 
                 estado_inicial=None, estados_finais=None, 
                 nome="AFD"):
        """Inicializa um AFD."""
        super().__init__(estados, alfabeto, transicoes, estado_inicial, estados_finais, nome)
        self.deterministic = True
    
    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        """Adiciona uma transição ao AFD."""
        self.adicionar_transicao_afd(estado_origem, simbolo, estado_destino)
    
    def executar(self, cadeia):
        """
        Simula a execução da cadeia no autômato.
        
        Args:
            cadeia (str): Cadeia de entrada a ser processada.
            
        Returns:
            bool: True se a cadeia for aceita, False caso contrário.
        """
        estado_atual = self.estado_inicial
        
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False  # Símbolo não está no alfabeto
            
            estado_atual = self.obter_transicao_afd(estado_atual, simbolo)
            
            if estado_atual is None:
                return False  # Não há transição definida
        
        # Verificar se o estado final é um estado de aceitação
        return estado_atual in self.estados_finais
    
    def executar_com_historico(self, cadeia):
        """
        Simula a execução da cadeia no autômato e retorna o histórico de estados.
        
        Args:
            cadeia (str): Cadeia de entrada a ser processada.
            
        Returns:
            tuple: (aceito, historico)
                - aceito (bool): True se a cadeia for aceita, False caso contrário.
                - historico (list): Lista de tuplas (estado, símbolo_lido) do processamento.
        """
        estado_atual = self.estado_inicial
        historico = [(estado_atual, None)]  # Estado inicial sem símbolo lido
        
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False, historico  # Símbolo não está no alfabeto
            
            estado_atual = self.obter_transicao_afd(estado_atual, simbolo)
            
            if estado_atual is None:
                return False, historico  # Não há transição definida
            
            historico.append((estado_atual, simbolo))
        
        # Verificar se o estado final é um estado de aceitação
        aceito = estado_atual in self.estados_finais
        return aceito, historico


class AutomatoFinitoNaoDeterministico(AutomatoFinito):
    """
    Classe para representação específica de Autômatos Finitos Não-Determinísticos (AFN).
    Herda da classe AutomatoFinito e adiciona funcionalidades específicas de AFNs.
    """
    
    def __init__(self, estados=None, alfabeto=None, transicoes=None, 
                 estado_inicial=None, estados_finais=None, 
                 nome="AFN"):
        """Inicializa um AFN."""
        super().__init__(estados, alfabeto, transicoes, estado_inicial, estados_finais, nome)
        self.deterministic = False
    
    def adicionar_transicao(self, estado_origem, simbolo, estado_destino):
        """Adiciona uma transição ao AFN."""
        self.adicionar_transicao_afn(estado_origem, simbolo, estado_destino)
    
    def obter_epsilon_fecho(self, estados):
        """
        Calcula o ε-fecho para um conjunto de estados.
        
        Args:
            estados (set ou str/int): Conjunto de estados ou um único estado.
            
        Returns:
            set: ε-fecho dos estados.
        """
        if isinstance(estados, (str, int)):  # Se for um único estado
            estados = {estados}
        
        fecho = set(estados)  # Inicializar com os estados de entrada
        pilha = list(estados)  # Usar uma pilha para processamento
        
        while pilha:
            estado = pilha.pop()
            for novo_estado in self.obter_transicoes_afn(estado, "ε"):
                if novo_estado not in fecho:
                    fecho.add(novo_estado)
                    pilha.append(novo_estado)
        
        return fecho
    
    def executar(self, cadeia):
        """
        Simula a execução da cadeia no autômato.
        
        Args:
            cadeia (str): Cadeia de entrada a ser processada.
            
        Returns:
            bool: True se a cadeia for aceita, False caso contrário.
        """
        # Conjunto de estados atuais, começando com o ε-fecho do estado inicial
        estados_atuais = self.obter_epsilon_fecho(self.estado_inicial)
        
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False  # Símbolo não está no alfabeto
            
            proximos_estados = set()
            
            # Para cada estado atual, calcular as transições possíveis
            for estado in estados_atuais:
                # Obter todos os estados alcançáveis com o símbolo atual
                estados_destino = self.obter_transicoes_afn(estado, simbolo)
                proximos_estados.update(estados_destino)
            
            # Calcular o ε-fecho dos próximos estados
            estados_atuais = set()
            for estado in proximos_estados:
                estados_atuais.update(self.obter_epsilon_fecho(estado))
            
            if not estados_atuais:
                return False  # Não há transições possíveis
        
        # Verificar se algum dos estados atuais é um estado de aceitação
        return any(estado in self.estados_finais for estado in estados_atuais)
    
    def executar_com_historico(self, cadeia):
        """
        Simula a execução da cadeia no autômato e retorna o histórico de estados.
        
        Args:
            cadeia (str): Cadeia de entrada a ser processada.
            
        Returns:
            tuple: (aceito, historico)
                - aceito (bool): True se a cadeia for aceita, False caso contrário.
                - historico (list): Lista de tuplas (conjunto_estados, símbolo_lido) do processamento.
        """
        # Conjunto de estados atuais, começando com o ε-fecho do estado inicial
        estados_atuais = self.obter_epsilon_fecho(self.estado_inicial)
        historico = [(estados_atuais, None)]  # Estado inicial sem símbolo lido
        
        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False, historico  # Símbolo não está no alfabeto
            
            proximos_estados = set()
            
            # Para cada estado atual, calcular as transições possíveis
            for estado in estados_atuais:
                # Obter todos os estados alcançáveis com o símbolo atual
                estados_destino = self.obter_transicoes_afn(estado, simbolo)
                proximos_estados.update(estados_destino)
            
            # Calcular o ε-fecho dos próximos estados
            estados_atuais = set()
            for estado in proximos_estados:
                estados_atuais.update(self.obter_epsilon_fecho(estado))
            
            historico.append((estados_atuais, simbolo))
            
            if not estados_atuais:
                return False, historico  # Não há transições possíveis
        
        # Verificar se algum dos estados atuais é um estado de aceitação
        aceito = any(estado in self.estados_finais for estado in estados_atuais)
        return aceito, historico