import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx
import math
from matplotlib.animation import FuncAnimation

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

    def _nodeCoord(self):
        #Calcula posições dos nós para visualização 2D
        pos = {}
        cuboMeio = {
            0: (0, self.N + 1),      # Norte
            1: (self.N + 1, 0),      # Leste  
            2: (0, -self.N - 1),     # Sul
            3: (-self.N - 1, 0)      # Oeste
        }
        
        for node in self.EN.nodes:
            cubo = self.EN.nodes[node]['cubo']
            coords = self.EN.nodes[node]['coords']
            projX, projY = cuboMeio[cubo]
            pos[node] = (coords[0] + projX, coords[1] + projY)
            
        return pos

class visualizar:
    def __init__(self, random_walk, iter=200):
        self.rw = random_walk
        self.iter = iter
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.pos = self.rw._nodeCoord()
        
        self.cubo_colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon'] # Cores para diferentes cubos
        self.atualPonto = None
        self.line = None
        self.textPasso = None
        
    def setup_plot(self):
        """Configura o plot inicial"""
        self.ax.clear()
        
        # Desenha os cubos
        for cubo in range(4):
            # Nos do cubo
            nodeCubos = [node for node in self.rw.EN.nodes 
                         if self.rw.EN.nodes[node]['cubo'] == cubo]
            
            # Desenha arestas do cubo
            arestasCubo = [(u, v) for u, v in self.rw.EN.edges() 
                         if u in nodeCubos and v in nodeCubos]
            
            nx.draw_networkx_edges(self.rw.EN, self.pos, edgelist=arestasCubo,
                                 ax=self.ax, edge_color='gray', alpha=0.6)
            
            # Desenha nós do cubo
            nx.draw_networkx_nodes(self.rw.EN, self.pos, nodelist=nodeCubos,
                                 node_color=self.cubo_colors[cubo], 
                                 node_size=50, alpha=0.7, ax=self.ax)
        
        # Desenha arestas entre cubos (conexões)
        arestasCuboInter = []
        for u, v in self.rw.EN.edges():
            cubo_u = self.rw.EN.nodes[u]['cubo']
            cubo_v = self.rw.EN.nodes[v]['cubo']
            if cubo_u != cubo_v:
                arestasCuboInter.append((u, v))
        
        nx.draw_networkx_edges(self.rw.EN, self.pos, edgelist=arestasCuboInter,
                             ax=self.ax, edge_color='red', style='--', alpha=0.8)
        
        # Configurações do plot
        self.ax.set_title('Passeio Aleatório Metaestável\nVisualização em Tempo Real', fontsize=16, pad=20)
        self.ax.axis('equal')
        self.ax.grid(True, alpha=0.3)
        
        # Legenda
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                      markersize=10, label='Cubo 0 (Norte)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                      markersize=10, label='Cubo 1 (Leste)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral', 
                      markersize=10, label='Cubo 2 (Sul)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightsalmon', 
                      markersize=10, label='Cubo 3 (Oeste)'),
            plt.Line2D([0], [0], color='red', linestyle='--', label='Conexões entre cubos'),
            plt.Line2D([0], [0], marker='o', color='red', markersize=10, label='Posição atual'),
            plt.Line2D([0], [0], color='blue', linewidth=2, label='Caminho percorrido')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right')
        
        # Inicializa elementos de animação
        self.atualPonto, = self.ax.plot([], [], 'ro', markersize=12, label='Posição Atual')
        self.line, = self.ax.plot([], [], 'b-', alpha=0.7, linewidth=2, label='Caminho')
        self.textPasso = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                    fontsize=12, verticalalignment='top',
                                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return self.atualPonto, self.line, self.textPasso
    
    def animate_step(self, frame):
        """Atualiza a animação para cada frame"""
        if frame == 0:
            # Reinicia a simulação
            self.rw.inicio(0)
            self.rw.caminho = [self.rw.estadoAtual]
        elif frame <= self.iter:
            # Executa um passo
            self.rw.andar()
        
        # Atualiza visualização
        if self.rw.caminho:
            # Pega coordenadas do caminho
            camCoord = [self.pos[node] for node in self.rw.caminho]
            x_vals, y_vals = zip(*camCoord) if camCoord else ([], []) #faz a projeção dos x em x_vals e de y em y_vals como lista
            
            # Atualiza linha do caminho
            self.line.set_data(x_vals, y_vals)
            
            # Atualiza ponto atual
            posAtual = self.pos[self.rw.estadoAtual]
            self.atualPonto.set_data([posAtual[0]], [posAtual[1]])
            
            # Atualiza texto
            cubo_atual = self.rw.EN.nodes[self.rw.estadoAtual]['cubo']
            coords_atual = self.rw.EN.nodes[self.rw.estadoAtual]['coords']
            self.textPasso.set_text(f'Passo: {frame}/{self.iter}\nCubo: {cubo_atual}\nCoords: {coords_atual}')
        
        return self.atualPonto, self.line, self.textPasso
    
    def animate(self, interval=100):
        """Cria e exibe a animação"""
        self.setup_plot()
        anim = FuncAnimation(self.fig, self.animate_step, frames=self.iter+1,
                           interval=interval, blit=True, repeat=True)
        plt.tight_layout()
        plt.show()
        return anim

if __name__ == "__main__":
    # Parâmetros da simulação
    N = 4  # Tamanho do cubo
    d = 2  # Dimensão
    iter = 2000  # Número de passos para animação
    
    print("Criando passeio aleatório metaestável...")
    rw = MetastableRandomWalk(N, d)
    
    print("Iniciando visualização animada...")
    print("Configuração:")
    print(f"- {N}x{N} pontos por cubo")
    print(f"- 4 cubos conectados")
    print(f"- {iter} passos da animação")
    print("\nA animação será iniciada...")
    
    visualizer = visualizar(rw, iter)
    anim = visualizer.animate(interval=150)  # Intervalo em milissegundos