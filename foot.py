import math
import numpy as np
import matplotlib.pyplot as plt 

t_inicio = 0
t_fim = 4
passo = 0.01
T = 1 

t_b = 0.4
t_e = 0.6
phi_b = t_b / T
phi_e = t_e / T

vetor_tempo = np.arange(t_inicio, t_fim, passo)


def v(phi):
    if phi < phi_b or phi >= phi_e:
        return 0
    else:
        return 0.5 * (1 - math.cos(2 * math.pi * (phi - phi_b) / (phi_e - phi_b)))


def v_ponto(phi):
    if phi < phi_b or phi >= phi_e:
        return 0
    else: 
        return 0.5 * (math.sin(2 * math.pi * (phi - phi_b) / (phi_e - phi_b)))

z_a = []
zponto_a = []
z_cm = 0
z_step = 1


for tempo in vetor_tempo:
    phi = tempo % T  
    z_a.append(z_cm + z_step * v(phi))
    zponto_a.append(z_step * v_ponto(phi))


plt.plot(vetor_tempo, z_a, label='z_a')  
plt.plot(vetor_tempo, zponto_a, label='zPonto_a')  
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()
plt.show()


