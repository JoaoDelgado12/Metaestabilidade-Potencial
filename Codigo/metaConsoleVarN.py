import numpy as np
import random as rd
import math

qtd = int(input("Quantas simulações ? ")) # perguntar a quantidade de simulações 
qtdRODADA = int(input("Quantidade de tempo para cada passeia ? "))
TAMIni = int(input("Qual o tamanho da inicial da cadeia ? "))# perguntar o tamanho inicial da cadeia de markov
vetorPadrao = [None] * TAMIni 
class Configuracao:
    icouple = set() #conj. de indice que estão em couple
    disponiveis = [i for i in range(TAMIni)] #conj. de indice
    def __init__(self, spin : int, vetor = None): #constrututor criando um configuração e inicializando com o spin (+ ou -)
        if vetor is None:
                self.conf = [spin for i in range(TAMIni)]
        else:
                self.conf = vetor


    @classmethod
    def andar(cls, p1,p2):#Move uma posição aleatória 
        global TAMIni
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

        for i in range(0, TAMIni): #adiciona os indices que fizeram couple
            print(i, TAMIni, len(p1.conf))
            if p1.conf[i] == p2.conf[i]:
                Configuracao.icouple.add(i)
        TAMIni += 1 
        cls.disponiveis.append(TAMIni - 1) #Aumenta o tamanho da cadeia
        p1.conf.append(rd.choice([1,-1]))
        p2.conf.append(rd.choice([1,-1]))
        
    @classmethod
    def reiniciar(cls, p1, p2, vetor1 = None, vetor2 = None ):
        TAMIni = len(vetorPadrao)
        cls.disponiveis = [i for i in range(TAMIni)]
        if vetor1 is not None and vetor2 is not None:
            Configuracao.icouple.clear()
            for i in range(0,TAMIni):
                p1.conf[i] = vetor1[i]
                p2.conf[i] = vetor2[i]
        elif vetor1 is not None :
            Configuracao.icouple.clear()
            for i in range(0,TAMIni):
                p1.conf[i] = vetor1[i]
                p2.conf[i] = -1
        elif vetor2 is not None :
            Configuracao.icouple.clear()
            for i in range(0,TAMIni):
                p1.conf[i] = +1
                p2.conf[i] = vetor2[i]
        else:
            Configuracao.icouple.clear()
            for i in range(0,TAMIni):
                p1.conf = [+1 for i in range(TAMIni)]
                p1.conf = [-1 for i in range(TAMIni)]
         

# ========= MAIN ============
p1 = Configuracao(+1)
p2 = Configuracao(-1)
media = 0
desP = 0
simulacao = [0 for i in range(0,qtd)]
Tempo : int = 0 #tempo

for i in range(0,qtd):    
    while(Tempo < qtdRODADA):
        Configuracao.andar(p1,p2)
        Tempo+= 1

    simulacao[i] = Tempo
    media += Tempo/len(simulacao)
    Configuracao.reiniciar(p1,p2)
    Tempo = 0
    print(i)

for i in range(0,qtd):
    desP += (simulacao[i] - TAMIni*math.log(TAMIni))**2
desP = math.sqrt(desP)/qtd

print("\n" + "="*50)
print("🎉 TODAS AS BOLINHAS ESTÃO VERDES!")
print("="*50)
print(f"⏱️  Tempo esperado: " + format(math.log(TAMIni)*TAMIni,'.2f') + " passos e \n" + 
"a media das simulações :" + format(media, '.2f') + " passos \n" +
"o desvio padrão  é " + format(desP, '.2f') )
print("="*50)



    

          
             