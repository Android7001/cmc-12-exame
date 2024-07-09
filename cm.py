import numpy as np
import math

# Defina os parâmetros do vetor de tempo
tempo_inicial = 0  # início do intervalo de tempo
tempo_final = 1    # final do intervalo de tempo
intervalo = 0.01   # intervalo de tempo em segundos (10^-2 segundos)

# Crie o vetor de tempo usando numpy
vetor_tempo = np.arange(tempo_inicial, tempo_final + intervalo, intervalo)

#print(vetor_tempo)

p = []
Vx = 1
Vy = 0
Vphi = 0
h = 0.5
g = 9.81
T = 1
tb = 0.4
te = 0.6
x0 = Vx * T / 2
xf = 3 * Vx * T / 2
p0 = Vx * T / 2
ps = Vx * T
pf = 3 * Vx * T / 2

for i in range(len(vetor_tempo)):
    if vetor_tempo[i] <= tb:
        p.append(Vx*T/2 + 5/4*Vx*T*vetor_tempo[i])
    elif vetor_tempo[i] >= tb and vetor_tempo[i] <= te:
        p.append(Vx*T)
    elif vetor_tempo[i] > te:
        p.append(Vx*T + 5/4*Vx*T*(vetor_tempo[i] - te))

print(p)

lamb = math.sqrt(h / g)

K0 = x0 - p0 + 5/4*Vx*T/lamb*math.sinh(-lamb*tb)

Kf = xf - pf + 5/4*Vx*T/lamb*math.sinh(-lamb*(T - te))

As = (Kf - K0*math.exp(-lamb*T)) / (math.exp(lamb*T) + math.exp(-lamb*T))

Bs = (K0*math.exp(lamb*T) - Kf) / (math.exp(lamb*T) + math.exp(-lamb*T))

x = []

for i in range(len(vetor_tempo)):
    if vetor_tempo[i] <= tb:
        x.append(p[i] + As*math.exp(lamb*T) + Bs*math.exp(-lamb*T) - 5/4*Vx*T/lamb*math.sinh(-lamb*tb))
    elif vetor_tempo[i] >= tb and vetor_tempo[i] <= te:
        x.append(p[i] + As*math.exp(lamb*T) + Bs*math.exp(-lamb*T))
    elif vetor_tempo[i] > te:
        x.append(p[i] + As*math.exp(lamb*T) + Bs*math.exp(-lamb*T) - 5/4*Vx*T/lamb*math.sinh(-lamb*(T-te)))

print(x)