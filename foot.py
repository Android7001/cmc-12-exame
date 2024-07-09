import math
import numpy as np
import matplotlib.pyplot as plt 

t_inicio = 0
t_fim = 1
passo = 0.01
T = 1 

t_b = 0.1
t_e = 0.9
phi_b = t_b / T
phi_e = t_e / T

vetor_tempo = np.arange(t_inicio, t_fim, passo)


def get_f(phi):
    if phi <= phi_b:
        return 0
    elif phi > phi_b and phi <= phi_e:
        return 0.5 * (1 - math.cos(math.pi * (phi - phi_b) / (phi_e - phi_b)))
    else:
        return 1

def get_g(phi):
    if phi <= phi_b or phi > phi_e:
        return 0
    else:
        return 0.5 * (1 - math.cos(2 * math.pi * (phi - phi_b) / (phi_e - phi_b)))


F = []
G = []
z_a = []
zponto_a = []
z_cm = 2
z_step = 1


for tempo in vetor_tempo:
    phi = tempo % T  
    f = get_f(phi)  # É o vponto(phi)
    g = get_g(phi)  # É o v(phi) 
    F.append(f)
    G.append(g)
    z_a.append(z_cm - z_step * g)
    zponto_a.append(-z_step * f)


plt.plot(vetor_tempo, G, label='g')  
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()
plt.show()


