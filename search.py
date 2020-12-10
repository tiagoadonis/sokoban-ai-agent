# from abc import ABC, abstractmethod
from operator import *

# Dominios de pesquisa (classe abstracta) -> implementar os métodos do SearchDomain no ficheiro 'student.py'
class SearchDomain():
    # Construtor
    # @abstractmethod
    def __init__(self):
        pass

    # Lista de ações possíveis num estado (linha, coluna) pode ir para (linha, coluna + 1), para (linha + 1, coluna)
    # (linha - 1, coluna) ou (linha, coluna - 1) se for possivel, pode ter paredes!!!
    # @abstractmethod
    def actions(self, state):
        pass

    # Resultado de uma ação num estado, ou seja, o estado seguinte
    # @abstractmethod
    def result(self, state, action):
        pass

    # Custo de uma ação num estado
    # @abstractmethod
    def cost(self, state, action):
        pass

    # Custo estimado de chegar do estado atual ao objetivo
    # @abstractmethod
    def heuristic(self, state, goal_state):
        pass

# Problemas concretos a resolver dentro de um determinado dominio
class SearchProblem:
    # Construtor
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal

    # Verifica se já se encontra no objetivo
    def goal_test(self, state):
        # print("ENTROU GOAL TEST -> "+str(len(self.domain.boxes) == self.domain.mapa.on_goal))
        return len(self.domain.boxes) == self.domain.mapa.on_goal

# Nós da árvore de pesquisa do Sokoban
class SokobanNode:
    # Construtor
    def __init__(self, state, parent, cost, heuristic):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        if self.parent != None :
            self.depth = self.parent.depth + 1
        else: 
            self.depth = 0

    # Método toString
    def __str__(self):
        return "["+ str(self.state) + " - " + str(self.heuristic) + " - " + str(self.cost) + "]"
    
    # Define a representação em cadeia de caractéres que aparece na consola do interpretador
    def __repr__(self):
        return str(self)

    def in_parent(self,state):
        if self.state == state:
            return True

# Árvore de Pesquisa
class SokobanTree:
    # Construtor
    def __init__(self, problem):
        self.problem = problem
        root = SokobanNode(problem.initial, None, 0, problem.domain.heuristic(problem.initial, problem.goal))
        self.open_nodes = [root]
        self.solution = None

    # Obter o caminho (sequencia de estados) da raiz ate um nó
    def get_path(self, node):
        print("ENTROU GET PATH")
        move = []
        if node.parent == None:
            return []
        # Cria uma lista com o path desde a raiz até ao destino
        path = self.get_path(node.parent, sokoban)
        move = list(map(sub, node.state[0], node.parent.state[0]))
        if (move == [1, 0]):
            key = 'd'
        elif (move == [-1, 0]):
            key = 'a'
        elif (move == [0, 1]):
            key = 's'
        elif (move == [0, -1]):
            key = 'w'
        else:
            key = ''
        path += [key]
        return path

    # Procurar a Solução
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                print("ACHOU SOLUÇÃO")
                self.solution = node
                return self.get_path(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                # print("NEWSTATE: "+str(newstate))
                newnode = SokobanNode(newstate, node, self.problem.domain.cost(node.state, a), self.problem.domain.heuristic(newstate, self.problem.goal))
                # print("NEWNODE: "+str(newnode))
                # Previne a criação de ciclos
                if not node.in_parent(newnode.state):
                    lnewnodes += [newnode]
            self.add_to_open(lnewnodes)
        return None

    # Define a estratégia
    def add_to_open(self,lnewnodes):
        # A* strategy
        self.open_nodes = sorted(self.open_nodes + list(lnewnodes), key=lambda n: n.cost + n.heuristic)