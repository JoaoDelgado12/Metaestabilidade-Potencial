import numpy as np
import random as rd
import math

qtd = int(input("Quantas simulações ?")) # perguntar a quantidade de simulações 
TAM = int(input("Qual o tamanho da cadeia ?"))# perguntar o tamanho da cadeia de markov

class Configuracao:
    icouple = set() #conj. de indice que estão em couple
    disponiveis = [i for i in range(0,TAM)] #conj. de indice
    def __init__(self, spin : int, vetor = None): #constrututor criando um configuração e inicializando com o spin (+ ou -)
            if vetor is None:
                 self.conf = [spin for i in range(TAM)]
            else:
                 self.conf = vetor


    @classmethod
    def andar(cls, p1,p2):#Move uma posição aleatória 
            i1 = rd.choice(Configuracao.disponiveis)#escolhendo o indice
            i2 = rd.choice(Configuracao.disponiveis)

            if i1 in Configuracao.icouple:
                p1.conf[i1] = rd.choice([1,-1]) #escolhendo o spin do indice in couple
                p2.conf[i1] = p1.conf[i1]
            elif i1 not in Configuracao.icouple : 
                p1.conf[i1] = rd.choice([1,-1]) #escolhendo o spin do indice

            if i2 in Configuracao.icouple:
                p2.conf[i2] = rd.choice([1,-1]) #escolhendo o spin do indice in couple
                p1.conf[i2] = p2.conf[i2]
            elif i2 not in Configuracao.icouple : 
                p1.conf[i2] = rd.choice([1,-1]) #escolhendo o spin do indice

            for i in range(0,TAM): #adiciona os indices que fizeram couple
                if p1.conf[i] == p2.conf[i]:
                    Configuracao.icouple.add(i)
    @classmethod
    def reiniciar(cls, p1, p2, vetor1 = None,vetor2 = None ):
        if vetor1 is not None and vetor2 is not None:
            Configuracao.icouple.clear()
            for i in range(0,TAM):
                p1.conf[i] = vetor1[i]
                p2.conf[i] = vetor2[i]
        elif vetor1 is not None :
            Configuracao.icouple.clear()
            for i in range(0,TAM):
                p1.conf[i] = vetor1[i]
                p2.conf[i] = -1
        elif vetor2 is not None :
            Configuracao.icouple.clear()
            for i in range(0,TAM):
                p1.conf[i] = +1
                p2.conf[i] = vetor2[i]
        else:
            Configuracao.icouple.clear()
            for i in range(0,TAM):
                p1.conf[i] = +1
                p2.conf[i] = -1
         

# ========= MAIN ============
p1 = Configuracao(+1)
p2 = Configuracao(-1)
media = 0
desP = 0
simulacao = [0 for i in range(0,qtd)]
Tempo : int = 0 #tempo

for i in range(0,qtd):    
    while(len(Configuracao.icouple) < TAM):
        Configuracao.andar(p1,p2)
        Tempo+= 1

    simulacao[i] = Tempo
    media += Tempo/len(simulacao)
    Configuracao.reiniciar(p1,p2)
    Tempo = 0

for i in range(0,qtd):
    desP += (simulacao[i] - TAM*math.log(TAM))**2
desP = math.sqrt(desP)/qtd

print("\n" + "="*50)
print("🎉 TODAS AS BOLINHAS ESTÃO VERDES!")
print("="*50)
print(f"⏱️  Tempo esperado: " + format(math.log(TAM)*TAM,'.2f') + " passos e \n" + 
"a media das simulações :" + format(media, '.2f') + " passos \n" +
"o desvio padrão  é " + format(desP, '.2f') )
print("="*50)



    

          
             