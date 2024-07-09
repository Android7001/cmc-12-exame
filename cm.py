import numpy as np
import math

# Defina os parâmetros do vetor de tempo
tempo_inicial = 0  # início do intervalo de tempo
tempo_final = 1    # final do intervalo de tempo
intervalo = 0.01   # intervalo de tempo em segundos (10^-2 segundos)

# Crie o vetor de tempo usando numpy
vetor_tempo = np.arange(tempo_inicial, tempo_final + intervalo, intervalo)

# Definindo os parâmetros da caminhada do robô
Vx = 1            # Velocidade no eixo x
Vy = 0            # Velocidade no eixo y (não utilizada no cálculo atual)
Vphi = 0          # Velocidade angular (não utilizada no cálculo atual)
h = 0.5           # Altura do centro de massa
g = 9.81          # Aceleração da gravidade
T = 1             # Período do passo
tb = 0.4          # Tempo inicial de suporte duplo
te = 0.6          # Tempo final de suporte duplo
x0 = Vx * T / 2   # Posição inicial
xf = 3 * Vx * T / 2  # Posição final
p0 = Vx * T / 2
ps = Vx * T
pf = 3 * Vx * T / 2
md1 = 5 / 4 * Vx * T
md2 = 5 / 4 * Vx * T

# Calculando p(t)
p = []
for t in vetor_tempo:
    if t <= tb:
        p.append(p0 + md1 * t)
    elif tb < t <= te:
        p.append(ps)
    else:
        p.append(ps + md2 * (t - te))

# Calculando lambda
lamb = math.sqrt(g / h)

# Calculando K0 e Kf
K0 = md1 / lamb * math.sinh(-lamb * tb)
Kf = md2 / lamb * math.sinh(lamb * (T - te))

# Calculando As e Bs
As = (Kf - K0 * math.exp(-lamb * T)) / (math.exp(lamb * T) + math.exp(-lamb * T))
Bs = (K0 * math.exp(lamb * T) - Kf) / (math.exp(lamb * T) + math.exp(-lamb * T))

# Calculando x(t)
x = np.zeros(len(vetor_tempo))
for i in range(len(vetor_tempo)):
    t = vetor_tempo[i]
    if t <= tb:
        x[i] = p[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1 / lamb) * math.sinh(-lamb * (t - tb))
    elif tb < t <= te:
        x[i] = p[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t)
    else:
        x[i] = p[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2 / lamb) * math.sinh(lamb * (t - te))

# Resultado
print(x)
