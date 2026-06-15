# 📓 Notas de Estudo: Metaestabilidade do ladim
> **Contexto:** Passeios aleatórios em grafos e cadeias de Markov de tempo contínuo.

---

## 🕒 1. Passeio aleatório em um grafo

A derivação da evolução assintótica do modelo *Coarse-grained* baseia-se nas propriedades do passeio aleatório em cubos discretos $E_N$.

* **Tempo de Mixing ($\tau_{mix}$):** Ordem de $N^2$.
  * *Significado:* Tempo necessário para o passeio esquecer sua condição inicial e atingir o equilíbrio local.
* **Tempo de Hitting das Bordas ($H_{\text{borda}}$):** 
  * $\mathbf{d = 2}$: Ordem de $N^2 \log N$.
  * $\mathbf{d \ge 3}$: Ordem de $N^d$.

> 💡 **Conclusão Crítica:** Como $\tau_{mix} \ll H_{\text{borda}}$, o passeio **termaliza** (atinge a distribuição quase-estacionária local) bem antes de alcançar as bordas do sistema.

---

## 🔍 2. A Filosofia do Modelo Coarse-Grained

O objetivo é reduzir a complexidade do sistema criando um "modelo resumido" em uma escala de tempo macroscópica $\alpha_N$.

* **Vizinhança Local ($V_N$):** Conjunto de pontos próximos a uma interseção $\xi$, definido pela distância limite $l_N$.
* **Escala Espacial:** A sequência $l_N$ cresce mais devagar que $N$ ($l_N \ll N$).
* **Dinâmica Transiente:** O tempo que o passeio gasta tentando sair de $V_N$ é desprezível. 
* **Escala de Tempo $\alpha_N$:** Definida de forma que $\alpha_N \gg \tau_{mix}$.

> 🎯 **Insight:** Embora o passeio original não seja globalmente estacionário, a escala $\alpha_N$ nos permite estudar as transições de fase e mudanças de estado como se o processo estivesse localmente em equilíbrio em cada fase.

**Como existe esse pequeno tempo de flutuação, então podemos descartar a convergência por meio da topologia de Skorohod.**

---

## 🧮 3. Formalização Matemática do Modelo Reduzido (Metaestabilidade)

Seja $\eta_N(t)$ uma cadeia de Markov de tempo contínuo, irredutível, com valores no espaço de estados finito $E_N$. 

### Gerador Infinitesimal
O operador gerador $L_N$ aplicado a uma função teste $f: E_N \to \mathbb{R}$ é dado por:

$$L_N f(\eta) = \sum_{\xi \in E_N} R_N(\eta, \xi) \big[ f(\xi) - f(\eta) \big]$$

* $R_N(\eta, \xi)$: Taxa (ou peso) de pulo do estado $\eta$ para o estado $\xi$.
* O passeio é **simétrico**, o que implica em escolha uniforme entre os vizinhos no momento do salto.

---
Tomando que para $E_{N}$ contém n **Valleys**, *$\lambda^{1}_{N}$*, *$\lambda^{2}_{N}$*, .... .Separando assim os $\delta_{N}$ (lembrando que isso é o conjunto dos pontos fora dos valleys). Pdemos definir uma função, tomando um observador $\phi_N(\eta)$ tal que seus valores são {1,2,3,..., n} $\cup${**O**}, $$\Phi_N(\eta) := \sum_{k=1}^n k \chi_{\mathcal{E}_N^k}(\eta) + \mathfrak{d} \chi_{\Delta_N}(\eta) .$$


---

## 🛑 4. Tempos de Parada (Hitting Times)

Para um subconjunto não vazio de estados $A \subset E_N$, definimos os seguintes tempos fundamentais:

### 📥 Tempo de Chegada (Hitting Time)
O primeiro instante em que o processo entra no conjunto $A$:
$$H_A = \inf \{ t \ge 0 : \eta_N(t) \in A \}$$

### 🔄 Tempo de Retorno (Retrial / Return Time)
O primeiro tempo de chegada em $A$ após o primeiro salto da cadeia (onde $\tau_1$ é o instante do primeiro pulo):
$$H_A^+ = \inf \{ t > \tau_1 : \eta_N(t) \in A \}$$

### 📌 Pontos de Interseção
* $B$: Conjunto de todos os pontos de interseção do grafo.
* $H_B^N(\eta_N(t))$: Menor tempo necessário para o passeio atingir o conjunto de interseção $B$.

## Last passage
Para termos a convergência na topologia Skorohod, é preciso retirar as flutuações das transições. Para realiza esse processo iremos recordar o estado anterior do passeio.

*  Vamos definir $\eta_{N}(t-) = \lim_{s \to t, s < t} \eta_{N}(s)$.

### Vamos definir um passeio 
Seja $X^V_N(t)$ dado por
$$X^V_N(t) := \Phi_N(\eta_N(\mathfrak{v}_N(t))) .$$
onde 
$$\mathfrak{v}_N(t) = \begin{cases} t & \text{if } \eta_N(t) \in \mathcal{E}_N, \\ \mathfrak{w}_N(t) & \text{otherwise}, \end{cases}$$

e $\mathfrak{w}_N(t)$ representa o ultimo tempo que o passeio estava em $\mathcal{E}_N^k$:
$$\mathfrak{w}_N(t) := \sup\{s \le t : \eta_N(s) \in \mathcal{E}_N\} \quad \text{and} \quad \mathcal{E}_N := \bigcup_{k=1}^n \mathcal{E}_N^k .$$

Veja, que basicamente esse processo só olha para dentro do valley como queriamos, permite o caminha da particula, porém ao sair do valley, o observador fixa no ultimo momento que ela esteve no valley até chegar no outro valley. Lembramndo que como esse tempo fora do valley é irrisório, então não perdemos muita informação.


Outra forma de definir $X^V_N(t)$ é:
$$T_{j+1} = \inf \big\{ t \ge T_j : \Phi(\eta_N(t)) \in S \setminus \{ \Phi(\eta_N(T_j)) \} \big\} , \quad j \ge 0 .$$

Assim, $T_{j+1}$ é primeiro tempo depois de uma mudança de estado depois de $T_{j}$. Perceba que se tomarmos o intervalo $[T_{j}, T_{j+1})$ e aplicar $X^V_N(t)$ nesse intervalo, iremos ter $X^V_N(t) = \Phi_{N}(\eta_{N}(T_{j}))$ ou gernelarizando $X^V_N(t) = \sum_{j \geq 0} \Phi_{N}(\eta_{N}(T_{j})) \chi_{[T_{j}, T(j+1))}(t)$. 

Tomando essas sequências de tempo $T_{j}$ como $H_{\mathcal{E^{j}_{N}}}$, então conseguimos um passei de escala $\alpha_{N}$ se mantendo constante. Assim conseguimos uma convergência em nossa topologia Skorohod.