import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
import math

class MetastableRandomWalk:
    def __init__(self, N, d=2):
        self.N = N
        self.d = d
        self.EN = self._grafo()
        self.estadoAtual = None
        self.passo = 0
        self.caminho = []
    
    def _grafo(self):
        G = nx.Graph()
        # Cria os 4 cubos (E0, E1, E2, E3)
        total_points = 4 * (self.N**self.d - 1) #para cada cubo
        
        cuboPonto = {}
        
        # Para cada cubo (0: norte, 1: leste, 2: sul, 3: oeste)
        for cubo in range(4):
            cuboPonto[cubo] = []
            
            # Gera pontos do cubo d-dimensional da vez cube
            for i in range(self.N**self.d):
                coords = self._indexCoord(i)
                NodeId = f"{cubo}_{i}"
                G.add_node(NodeId, cubo=cubo, coords=coords)
                cuboPonto[cubo].append(NodeId)
        
        # Conecta as vizinhas de cada cubo dentro de cada curbo, mas não os pontos de intersecção
        for cubo in range(4):
            points = cuboPonto[cubo]
            for i, nodeOrin in enumerate(points):
                coords1 = self._indexCoord(i)
                # Encontra vizinhos no cubo
                for dim in range(self.d):
                    for delta in [-1, 1]:
                        vizin = coords1.copy()
                        vizin[dim] += delta
                        if 0 <= vizin[dim] < self.N:
                            j = self._coordIndex(vizin)
                            node2 = points[j]
                            G.add_edge(nodeOrin, node2)
        
        # Conecta cubos adjacentes (pontos de canto compartilhados)
        self._JuntarCubo(G, cuboPonto)
        
        return G
    
    def _indexCoord(self, index):
        #Converte índice linear para coordenadas d-dimensionais
        coords = []
        vindex = index
        for _ in range(self.d):
            coords.append(vindex % self.N)
            vindex //= self.N
        return coords
    
    def _coordIndex(self, coords):
        #Converte coordenadas d-dimensionais para índice linear
        index = 0
        potDim = 1
        for i, coord in enumerate(coords):
            index += coord * potDim
            potDim *= self.N
        return index
    
    def _JuntarCubo(self, G, vCuboPontos):
        #Ajunção dos cubos
        conecta = [(0, 1), (1, 2), (2, 3), (3, 0)]  # pares de cubos adjacentes
        
        conectaPonto = [(self.N-1, 0), (0, self.N-1), (0,0), (self.N-1,self.N-1),
                    (0, self.N-1), (self.N-1, 0), (self.N-1, self.N-1), (0, 0)] #Quem queremos ligar
        
        for i in range(0,8,2):
            pontos1 = vCuboPontos[conecta[int(i/2)][0]]
            pontos2 = vCuboPontos[conecta[int(i/2)][1]]
            
            indexNode1 = self._coordIndex(conectaPonto[i])
            indexNode2 = self._coordIndex(conectaPonto[i+1])

            print(indexNode1, indexNode2)

            G.add_edge(pontos1[indexNode1], pontos2[indexNode2])

    def inicio(self, start=0):
        #Inicializa o passeio aleatório em um cubo
        cuboPontos= [node for node in self.EN.nodes if self.EN.nodes[node]['cubo'] == start]
        procurando = True
        while(procurando):
            procurando = False
            self.estadoAtual = np.random.choice(cuboPontos)
            for i in range(2):
                if(self.EN.nodes[self.estadoAtual]['coords'][i] > self.N - ( math.floor( math.sqrt(self.N) ) )/2 ): #para começar no quadrado interno
                    procurando = True
                    break
                elif(self.EN.nodes[self.estadoAtual]['coords'][i] < ( math.floor( math.sqrt(self.N) ) )/2 ):
                    procurando = True
                    break
        self.passo = 0
        self.caminho = [self.estadoAtual]

    def andar(self):
            vizin = list(self.EN.neighbors(self.estadoAtual))
            self.estadoAtual = np.random.choice(vizin)
            self.passo += 1
            self.caminho.append(self.estadoAtual)
            
            return self.estadoAtual

    def simular(self, steps, start=0):
            self.inicio(start)
            
            for _ in range(steps):
                self.andar()
            
            return self.caminho

    def transicao(self):
        transicao = []
        for i in range(1, len(self.caminho)):
            atualCubo = self.EN.nodes[self.caminho[i-1]]['cubo']
            proxCubo = self.EN.nodes[self.caminho[i]]['cubo']
            if atualCubo != proxCubo:
                transicao.append((atualCubo, proxCubo))
        return transicao
    
    def compute(self):
        contCubo = defaultdict(int)
        trasincoes = self.transicao()
        
        # Tempo em cada cubo
        atualCubo = self.EN.nodes[self.caminho[0]]['cubo']
        tempoInicioCubo = 0
        
        for i in range(1, len(self.caminho)):
            cubo = self.EN.nodes[self.caminho[i]]['cubo']
            if cubo != atualCubo:
                tempoCubo = i - tempoInicioCubo
                contCubo[atualCubo] += tempoCubo
                atualCubo = cubo
                tempoInicioCubo = i
        
        # Último período de residência
        tempoCubo = len(self.caminho) - tempoInicioCubo
        contCubo[atualCubo] += tempoCubo
        
        # Taxas de transição
        contTrasicao = defaultdict(int)
        for cuboOrin, cuboTo in trasincoes:
            contTrasicao[(cuboOrin, cuboTo)] += 1
        
        return contCubo, contTrasicao
   

if __name__ == "__main__":
    # Parâmetros da simulação
    N = 10  # Tamanho do cubo
    d = 2  # Dimensão
    iter = 1000
    
    print("Simulando passeio aleatório metaestável...")
    print(f"Parâmetros: N={N}, d={d}, passos={iter}")
    
    # Cria e simula o passeio aleatório
    rw = MetastableRandomWalk(N, d)
    caminho = rw.simular(iter, 0)
    
    # Calcula métricas de metaestabilidade
    tempoCubo, transicao = rw.compute()
    
    print("\nTempos em cada cubo:")
    for cubo in range(4):
        print(f"Cubo {cubo}: {tempoCubo[cubo]} passos")
    
    print("\nTransições entre cubos:")
    for (cuboOrin, cuboTo), cont in transicao.items():
        print(f"{cuboOrin} -> {cuboTo}: {cont} vezes")
    
    # Análise adicional
    print(f"\nTotal de passos: {rw.passo}")
    print(f"Número de nós no grafo: {rw.EN.number_of_nodes()}")
    print(f"Número de arestas no grafo: {rw.EN.number_of_edges()}")

