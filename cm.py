import numpy as np
import math
import matplotlib.pyplot as plt

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
px0 = Vx * T / 2
pxs = Vx * T
pxf = 3 * Vx * T / 2
md1x = (pxs - px0) / tb
md2x = (pxf - pxs) / (T - te)

# Calculando p(t)
px = np.zeros(len(vetor_tempo))
for i in range(len(vetor_tempo)):
    if vetor_tempo[i] <= tb:
        px[i] = px0 + md1x * vetor_tempo[i]
    elif tb < vetor_tempo[i] <= te:
        px[i] = pxs
    else:
        px[i] = pxs + md2x * (vetor_tempo[i] - te)

# Calculando lambda
lamb = math.sqrt(g / h)

# Calculando K0 e Kf
K0 = md1x / lamb * math.sinh(-lamb * tb)
Kf = md2x / lamb * math.sinh(lamb * (T - te))

# Calculando As e Bs
As = (Kf - K0 * math.exp(-lamb * T)) / (math.exp(lamb * T) - math.exp(-lamb * T))
Bs = (K0 * math.exp(lamb * T) - Kf) / (math.exp(lamb * T) - math.exp(-lamb * T))

# Calculando x(t)
x = np.zeros(len(vetor_tempo))
for i in range(len(vetor_tempo)):
    t = vetor_tempo[i]
    if t <= tb:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1x / lamb) * math.sinh(lamb * (t - tb))
    elif tb < t <= te:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t)
    else:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2x / lamb) * math.sinh(lamb * (t - te))

# Plotando x(t) ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(vetor_tempo, x, label='Posição do Centro de Massa (x)', color='b')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição do Centro de Massa ao Longo do Tempo')
plt.legend()
plt.grid(True)
plt.show()
