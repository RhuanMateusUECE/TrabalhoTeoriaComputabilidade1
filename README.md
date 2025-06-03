# 🤖 Simulador de Autômatos Finitos

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)

> **Implementação completa de simulação de autômatos finitos com operações e gramática linear à direita**

Este projeto implementa um simulador educacional que converte **Gramáticas Lineares Unitárias à Direita (GLUD)** em **Autômatos Finitos** e aplica as principais operações de fechamento estudadas em Teoria da Computação.

---

## 📋 Sumário

- [Características](#-características)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Etapas do Processo](#-etapas-do-processo)
- [Formato de Entrada](#-formato-de-entrada)
- [Exemplos](#-exemplos)
- [Arquivos Gerados](#-arquivos-gerados)
- [Algoritmos Implementados](#-algoritmos-implementados)
- [Contribuição](#-contribuição)

---

## ✨ Características

- ✅ **Conversão Gramática → AFN** (Autômato Finito Não-determinístico)
- ✅ **Determinização AFN → AFD** (Algoritmo de Subconjuntos)
- ✅ **Operação de Reverso** com normalização automática
- ✅ **Operação de Complemento** 
- ✅ **Simulação de cadeias** em todos os autômatos
- ✅ **Interface amigável** com saída detalhada
- ✅ **Geração automática** de arquivos de resultado
- ✅ **Validação de consistência** dos resultados

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Nenhuma dependência externa necessária

---

## ⚡ Uso Rápido

### 1. Criar arquivo de entrada
Crie um arquivo `entrada.txt` com sua gramática:

```
# Gramática: G = ({S, A}, {a, b}, P, S)
S -> aA
A -> bS
S -> ε
w = abab
```

### 2. Executar o simulador
```bash
python simulador_automatos.py
```

### 3. Verificar resultados
O programa gerará automaticamente:
- `AFN.txt` - Autômato Finito Não-determinístico
- `AFD.txt` - Autômato Finito Determinístico
- `REV.txt` - Autômato após operação de Reverso
- `COMP.txt` - Autômato após operação de Complemento

---

## 🔄 Etapas do Processo

### **ETAPA 1: Gramática → AFN**
Converte uma Gramática Linear Unitária à Direita em um Autômato Finito Não-determinístico.

**Algoritmo:**
- `X → aY` ⟹ `δ(X, a) → Y`
- `X → a` ⟹ `δ(X, a) → Z` (estado final)
- `X → ε` ⟹ `δ(X, ε) → Z`

### **ETAPA 2: AFN → AFD**
Aplica o algoritmo de determinização (subconjuntos) para eliminar não-determinismo.

**Características:**
- Usa ε-closure para lidar com transições vazias
- Estados do AFD são subconjuntos dos estados do AFN
- Garante equivalência de linguagens

### **ETAPA 3A: Operação de Reverso**
Gera autômato que reconhece a linguagem reversa L^R.

**Processo:**
1. Normalização (se |F| > 1): cria estado final único
2. Inversão: reverte todas as transições
3. Troca inicial ↔ final

### **ETAPA 3B: Operação de Complemento**
Gera autômato que reconhece o complemento da linguagem (Σ* - L).

**Algoritmo:**
- Mantém tudo igual, exceto estados finais
- `F_complemento = Q - F_original`

### **ETAPA 4: Simulação**
Testa cadeias de entrada em todos os autômatos gerados.

**Funcionalidades:**
- Simulação passo-a-passo
- Rastreamento do caminho percorrido
- Verificação de consistência entre operações

---

## 📝 Formato de Entrada

### Estrutura do arquivo `entrada.txt`:

```
# Comentários começam com #
# Definição da gramática (opcional)
G = ({S, A}, {a, b}, P, S)

# Produções (obrigatório)
S -> aA
A -> bS
S -> ε

# Cadeia de teste (opcional)
w = abab
```

### Regras:
- **Produções**: Uma por linha no formato `NaoTerminal -> producao`
- **Terminais**: Símbolos minúsculos (a, b, c, ...)
- **Não-terminais**: Símbolos maiúsculos (S, A, B, ...)
- **Palavra vazia**: Use `ε` ou deixe vazio após `->` 
- **Cadeia de teste**: Linha no formato `w = sua_cadeia`

---

## 💡 Exemplos

### Exemplo 1: Linguagem (ab)*
```
S -> abS
S -> ε
w = abab
```

### Exemplo 2: Linguagem a*b*
```
S -> aS
S -> bA
A -> bA
A -> ε
w = aaabbb
```

### Exemplo 3: Palavras com número par de a's
```
S -> aA
S -> bS
S -> ε
A -> aS
A -> bA
w = aabb
```

---

## 📁 Arquivos Gerados

### `AFN.txt`
```
# AFN Original
Q: A, S, Z
Σ: a, b
δ:
S, a -> A
A, b -> S
S, ε -> Z
S: inicial
F: Z
```

### `AFD.txt`
```
# AFD Determinizado
Q: {A}, {S, Z}, ∅
Σ: a, b
δ:
{S, Z}, a -> {A}
{A}, b -> {S, Z}
{S, Z}: inicial
F: {S, Z}
```

### `REV.txt` e `COMP.txt`
Seguem formato similar com suas respectivas modificações.

---

## 🧮 Algoritmos Implementados

### ε-closure (Fechamento Epsilon)
```python
def epsilon_closure(estados, delta):
    """Calcula todos os estados alcançáveis via transições ε"""
    # Implementação usando busca em profundidade
```

### Determinização (Algoritmo de Subconjuntos)
```python
def converter_afn_para_afd(afn):
    """Converte AFN em AFD equivalente"""
    # Usa ε-closure e construção de subconjuntos
```

### Operações de Fechamento
```python
def aplicar_operacao_reverso(afd):
    """Aplica operação de reverso: L → L^R"""
    
def aplicar_operacao_complemento(afd):
    """Aplica operação de complemento: L → Σ* - L"""
```

---

## 🎓 Conceitos Teóricos

Este simulador implementa os seguintes conceitos de **Teoria da Computação**:

- **Gramáticas Livres de Contexto** (subset: lineares à direita)
- **Autômatos Finitos Determinísticos e Não-determinísticos**
- **Equivalência entre Gramáticas e Autômatos**
- **Algoritmo de Determinização**
- **Operações de Fechamento Regular**
- **ε-transições** e **ε-closure**
- **Simulação de Autômatos**

---

## 🧪 Testes e Validação

### Verificações Automáticas
- ✅ Complemento deve ter resultado oposto ao original
- ✅ Reverso aceita cadeia invertida
- ✅ AFD e AFN equivalentes reconhecem mesma linguagem
- ✅ Estados finais corretamente identificados

### Executar Exemplos
```bash
# Usar arquivo de exemplo padrão
python simulador_automatos.py

# Testar com gramática personalizada
# 1. Edite entrada.txt com sua gramática
# 2. Execute novamente
```

---

## 👥 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas para Contribuição
- [ ] Interface gráfica (GUI)
- [ ] Mais operações de fechamento (união, interseção)
- [ ] Suporte a gramáticas mais complexas
- [ ] Otimização de algoritmos
- [ ] Testes unitários
- [ ] Documentação adicional

---

## 🐛 Reportar Bugs

Encontrou um bug? [Abra uma issue](https://github.com/RhuanMateusUECE/TrabalhoTeoriaComputabilidade1/issues) com:

- Descrição detalhada do problema
- Arquivo de entrada que causou o erro
- Saída esperada vs. obtida
- Versão do Python utilizada

---

## 👨‍💻 Autores

- **Rhuan Mateus Matias Filgueira**
- **Mardonio Hilbert**

**Curso:** Ciências da Computação
**Cadeira:** Teoria da Computabilidade  
**Professor:** Bonfim Amaro Junior  
**Instituição:** Universidade Estadual do Ceará
**Data:** Maio 2025

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela! ⭐**

[🏠 Página Inicial](https://github.com/RhuanMateusUECE/TrabalhoTeoriaComputabilidade1)

</div>
