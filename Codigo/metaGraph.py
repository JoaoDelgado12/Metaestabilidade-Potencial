import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random as rd
import math

TAM = 50  # constante do tamanho do vetor
Tempo: int = 0  # tempo

# Definindo o intervalo do eixo x
x = np.arange(0, TAM, 1)

class Configuracao:
    icouple = set()  # conj. de indice que estão em couple
    disponiveis = [i for i in range(TAM)]  # conj. de indice
    
    def __init__(self, spin: int, pos, neg):  # construtor criando um configuração e inicializando com o spin (+ ou -)
        self.conf = [spin for i in range(TAM)]
        if spin > 0:
            for i in range(0, TAM):
                pos[i].set_facecolor("red")
        else:
            for i in range(0, TAM):
                neg[i].set_facecolor("black")
    
    @classmethod 
    def visuaizar(cls, p1, p2, bolinhas1, bolinhas2):
        for i in range(0, TAM):
            if p1.conf[i] == p2.conf[i]:  # procurando o couple
                if p1.conf[i] > 0:
                    bolinhas1[i].set_facecolor("green")
                    bolinhas2[i].set_facecolor("white")
                else:
                    bolinhas1[i].set_facecolor("white")
                    bolinhas2[i].set_facecolor("green")
            else:
                if p1.conf[i] > 0:
                    bolinhas1[i].set_facecolor("red")
                else:
                    bolinhas1[i].set_facecolor("black")
                if p2.conf[i] > 0:
                    bolinhas2[i].set_facecolor("red")
                else:
                    bolinhas2[i].set_facecolor("black")
    
    @classmethod
    def andar(cls, p1, p2, bolinhas1, bolinhas2):  # Move uma posição aleatória 
        i1 = rd.choice(Configuracao.disponiveis)  # escolhendo o indice
        i2 = rd.choice(Configuracao.disponiveis)
        
        if i1 in Configuracao.icouple:
            p1.conf[i1] = rd.choice([1, -1])  # escolhendo o spin do indice in couple
            p2.conf[i1] = p1.conf[i1]
        elif i1 not in Configuracao.icouple: 
            p1.conf[i1] = rd.choice([1, -1])  # escolhendo o spin do indice
        
        if i2 in Configuracao.icouple and i2 != i1:
            p2.conf[i2] = rd.choice([1, -1])  # escolhendo o spin do indice in couple
            p1.conf[i2] = p2.conf[i2]
        elif i2 not in Configuracao.icouple: 
            p2.conf[i2] = rd.choice([1, -1])  # escolhendo o spin do indice
        
        for i in range(0, TAM):  # adiciona os indices que fizeram couple
            if p1.conf[i] == p2.conf[i]:
                Configuracao.icouple.add(i)
        
        Configuracao.visuaizar(p1, p2, bolinhas1, bolinhas2)

# === Definição do matplotlib ===
fig, ax = plt.subplots(figsize=(8, 4))

# Caminho 1
ax.hlines(y=1, xmin=0, xmax=TAM - 1, color="black", zorder=1, label="Eixo (-)")
ax.hlines(y=3, xmin=0, xmax=TAM - 1, color="red", zorder=1, label="Eixo (+)")

bolinhas2 = [ax.scatter(xi, 1, facecolors="white", edgecolors="black", s=100, zorder=2) for xi in x]
bolinhas1 = [ax.scatter(xi, 3, facecolors="white", edgecolors="black", s=100, zorder=2) for xi in x]

# Ajustes do gráfico
ax.set_xlim(-1, TAM)
ax.set_ylim(0, 8)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)

# === Função de atualização da animação ===
p1 = Configuracao(+1, bolinhas1, bolinhas2)
p2 = Configuracao(-1, bolinhas1, bolinhas2)

def update(frame):
    global Tempo
    Tempo += 1
    Configuracao.andar(p1, p2, bolinhas1, bolinhas2)
    if len(Configuracao.icouple) == TAM:
        print("\n" + "="*50)
        print("TODAS AS BOLINHAS ESTÃO VERDES!")
        print("="*50)
        print(f"Tempo total: {Tempo} segundos")
        print(f"Tempo esperado: {format(math.log(TAM)*TAM,'.2f')} segundos")
        print("="*50)
        anim.event_source.stop()
    return bolinhas1 + bolinhas2

# === Criação da animação ===
anim = FuncAnimation(fig, update, frames=200, interval=100, blit=False, repeat=True)

plt.show()