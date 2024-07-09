import math
import numpy as np

t_inicio = 0
t_fim = 1
passo = 0.01
T = 1 


t_b = 0.4
t_e = 0.6
psi_b = t_b / T
psi_e = t_e / T

vetor_tempo = np.arange(t_inicio, t_fim, passo)


def get_f(psi):
    if psi <= psi_b:
        return 0
    elif psi > psi_b and psi <= psi_e:
        return 0.5 * (1 - math.cos(math.pi * (psi - psi_b) / (psi_e - psi_b)))
    else:
        return 1

def get_g(psi):
    if psi <= psi_b or psi > psi_e:
        return 0
    else:
        return 0.5 * (1 - math.cos(2 * math.pi * (psi - psi_b) / (psi_e - psi_b)))


F = []
G = []


for tempo in vetor_tempo:
    psi = tempo % T  
    f = get_f(psi)
    g = get_g(psi)
    F.append(f)
    G.append(g)


print("F:", F)
print("G:", G)
