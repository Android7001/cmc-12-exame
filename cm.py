import numpy as np
import math
import matplotlib.pyplot as plt

# Defina os parâmetros do vetor de tempo
tempo_inicial = 0  # início do intervalo de tempo
tempo_final = 1  # final do intervalo de tempo
intervalo = 0.01  # intervalo de tempo em segundos (10^-2 segundos)

# Crie o vetor de tempo usando numpy
tempo = np.arange(tempo_inicial, tempo_final + intervalo, intervalo)

# Definindo os parâmetros da caminhada do robô
Vy = 0  # Velocidade no eixo y (não utilizada no cálculo atual)
Vphi = 0  # Velocidade angular (não utilizada no cálculo atual)
h = 0.5  # Altura do centro de massa
g = 9.81  # Aceleração da gravidade
T = 1  # Período do passo
tb = 0.4  # Tempo inicial de suporte duplo
te = 0.6  # Tempo final de suporte duplo

def get_Xcm(Vx, xi):

    px0 = Vx * T / 2
    pxs = Vx * T
    pxf = 3 * Vx * T / 2
    md1x = (pxs - px0) / tb
    md2x = (pxf - pxs) / (T - te)

    # Calculando px(t) (ZMP)
    px = np.zeros(len(tempo))
    for i in range(len(tempo)):
        if tempo[i] <= tb:
            px[i] = px0 + md1x * tempo[i]
        elif tb < tempo[i] <= te:
            px[i] = pxs
        else:
            px[i] = pxs + md2x * (tempo[i] - te)

    # Calculando lambda
    lamb = math.sqrt(g / h)

    # Calculando K0 e Kf
    K0 = md1x / lamb * math.sinh(-lamb * tb)
    Kf = md2x / lamb * math.sinh(lamb * (T - te))

    # Calculando As e Bs
    As = (Kf - K0 * math.exp(-lamb * T)) / (math.exp(lamb * T) - math.exp(-lamb * T))
    Bs = (K0 * math.exp(lamb * T) - Kf) / (math.exp(lamb * T) - math.exp(-lamb * T))

    # Calculando x(t)
    x = np.zeros(len(tempo))
    for i in range(len(tempo)):
        t = tempo[i]
        if t <= tb:
            x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1x / lamb) * math.sinh(
                lamb * (t - tb)) + xi
        elif tb < t <= te:
            x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) + xi
        else:
            x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2x / lamb) * math.sinh(
                lamb * (t - te)) + xi

    return x

def get_Ycm(Vy, yi):

    py0 = Vy * T / 2
    pys = Vy * T
    pyf = 3 * Vy * T / 2
    md1y = (pys - py0) / tb
    md2y = (pyf - pys) / (T - te)

    # Calculando px(t) (ZMP)
    py = np.zeros(len(tempo))
    for i in range(len(tempo)):
        if tempo[i] <= tb:
            py[i] = py0 + md1y * tempo[i]
        elif tb < tempo[i] <= te:
            py[i] = pys
        else:
            py[i] = pys + md2y * (tempo[i] - te)

    # Calculando lambda
    lamb = math.sqrt(g / h)

    # Calculando K0 e Kf
    K0 = md1y / lamb * math.sinh(-lamb * tb)
    Kf = md2y / lamb * math.sinh(lamb * (T - te))

    # Calculando As e Bs
    As = (Kf - K0 * math.exp(-lamb * T)) / (math.exp(lamb * T) - math.exp(-lamb * T))
    Bs = (K0 * math.exp(lamb * T) - Kf) / (math.exp(lamb * T) - math.exp(-lamb * T))

    # Calculando y(t)
    y = np.zeros(len(tempo))
    for i in range(len(tempo)):
        t = tempo[i]
        if t <= tb:
            y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1y / lamb) * math.sinh(
                lamb * (t - tb)) + yi
        elif tb < t <= te:
            y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) + yi
        else:
            y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2y / lamb) * math.sinh(
                lamb * (t - te)) + yi

    return x

x = get_Xcm(1, 2)

# Plotando x(t) ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(tempo, x, label='Posição do Centro de Massa (x)', color='b')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição do Centro de Massa ao Longo do Tempo')
plt.legend()
plt.grid(True)
plt.show()
