import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

class SingleCubeEscape:
    def __init__(self, N):
        self.N = N
        self.G = self._build_graph()
        self.reset()

        self.escapes = []   # tempos de saída
        self.attempt = 0

    def _build_graph(self):
        G = nx.grid_2d_graph(self.N, self.N) #cria um grid, mais prático que o graph 
        return G


    def reset(self):
        self.passo = 0
        self.caminho = []

        mid = self.N // 2 #Lembrando que sempre começa no meio
        self.estadoAtual = (mid, mid)

        self.caminho.append(self.estadoAtual)

    def is_boundary(self, node):
        x, y = node
        return x == 0 or y == 0 or x == self.N - 1 or y == self.N - 1

    def andar(self):
        vizinhos = list(self.G.neighbors(self.estadoAtual))
        self.estadoAtual = vizinhos[np.random.randint(len(vizinhos))]

        self.passo += 1
        self.caminho.append(self.estadoAtual)

        # condição de escape
        if self.is_boundary(self.estadoAtual):
            self.escapes.append(self.passo/((self.N-1)**2 * math.log(self.N-1)))
            self.attempt += 1
            self.reset()
            

    def simular(self, tentativas):
        for i in range(tentativas):
            print("Tentativa: " + str(i))
            while True:
                self.andar()
                if self.attempt > i:
                    break
        return self.escapes


    
def plot_resultados(escapes):
    plt.figure(figsize=(20,10))
    plt.plot(np.sort(escapes), range(1, len(escapes)+1) , marker='o' )
    plt.title("Tempo de saída do cubo por tentativa")
    plt.xlabel("Tempo de escape")
    plt.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    N = 1000
    tentativas = 100

    sim = SingleCubeEscape(N + 1)

    print("Rodando simulação...")
    escapes = sim.simular(tentativas)

    plot_resultados(escapes)